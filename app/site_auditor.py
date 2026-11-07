"""Small, polite, same-origin technical SEO crawler for OpenSite."""
from collections import Counter, deque
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag, urljoin, urlparse, urlunparse
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser
import ipaddress
import socket
import ssl
import time


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.description = ""
        self.canonical = ""
        self.robots = ""
        self.h1 = []
        self.h2 = []
        self.links = []
        self.images = []
        self.text_parts = []
        self._h2 = False
        self._skip_text_depth = 0
        self._title = False
        self._h1 = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("script", "style", "noscript", "svg"):
            self._skip_text_depth += 1
        if tag == "title": self._title = True
        if tag == "h1": self._h1 = True
        if tag == "h2": self._h2 = True
        if tag == "meta":
            name = (attrs.get("name") or "").lower()
            if name == "description": self.description = attrs.get("content", "").strip()
            if name == "robots": self.robots = attrs.get("content", "").strip()
        if tag == "link" and "canonical" in (attrs.get("rel") or "").lower().split(): self.canonical = attrs.get("href", "").strip()
        if tag == "a" and attrs.get("href"): self.links.append(attrs["href"])
        if tag == "img": self.images.append(attrs.get("alt", "").strip())

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "svg") and self._skip_text_depth:
            self._skip_text_depth -= 1
        if tag == "title": self._title = False
        if tag == "h1": self._h1 = False
        if tag == "h2": self._h2 = False

    def handle_data(self, data):
        if self._skip_text_depth:
            return
        text = " ".join(data.split())
        if not text: return
        if self._title: self.title += (" " if self.title else "") + text
        if self._h1: self.h1.append(text)
        if self._h2: self.h2.append(text)
        self.text_parts.append(text)


def _public_http_url(value):
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ValueError("Enter a full public http(s) URL.")
    if parsed.username or parsed.password:
        raise ValueError("URLs containing credentials are not accepted.")
    try:
        addresses = {item[4][0] for item in socket.getaddrinfo(parsed.hostname, parsed.port or (443 if parsed.scheme == "https" else 80))}
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve host: {exc}") from exc
    if not addresses or any(not ipaddress.ip_address(address).is_global for address in addresses):
        raise ValueError("The auditor only visits public internet hosts.")
    return parsed


def _normalise(url):
    parsed = urlparse(urldefrag(url).url)
    path = parsed.path or "/"
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), path, "", parsed.query, ""))


def crawl_site(start_url, max_pages=30, delay_seconds=0.15):
    """Crawl same-host HTML pages; cap scope and duration for a safe demo audit."""
    parsed_start = _public_http_url(start_url.strip())
    origin = (parsed_start.scheme, parsed_start.netloc.lower())
    root = _normalise(start_url)
    queue = deque([root])
    visited = set()
    pages = []
    errors = []
    context = ssl.create_default_context()
    robots = RobotFileParser()
    robots.set_url(f"{parsed_start.scheme}://{parsed_start.netloc}/robots.txt")
    try:
        robots.read()
    except (OSError, URLError, TimeoutError):
        robots = None
    while queue and len(pages) < max(1, min(int(max_pages), 100)):
        url = queue.popleft()
        url = _normalise(url)
        if url in visited: continue
        visited.add(url)
        try:
            parsed = _public_http_url(url)
            if (parsed.scheme, parsed.netloc.lower()) != origin: continue
            if robots and not robots.can_fetch("OpenSiteBot", url):
                errors.append({"url":url,"error":"Blocked by robots.txt"})
                continue
            request = Request(url, headers={"User-Agent": "OpenSiteBot/1.0 (+https://opensite.local; technical SEO audit)"})
            with urlopen(request, timeout=10, context=context) as response:
                status = response.status
                content_type = response.headers.get("Content-Type", "")
                final_url = response.geturl()
                if "text/html" not in content_type.lower(): continue
                body = response.read(1_500_000).decode(response.headers.get_content_charset() or "utf-8", errors="replace")
            page = PageParser()
            page.feed(body)
            body_text = " ".join(page.text_parts)
            item = {"url": final_url, "status": status, "title": page.title.strip(), "title_length": len(page.title.strip()),
                    "description": page.description, "description_length": len(page.description), "canonical": urljoin(final_url, page.canonical) if page.canonical else "",
                    "robots": page.robots, "h1": page.h1, "h2": page.h2, "images": len(page.images), "images_missing_alt": sum(not alt for alt in page.images),
                    "word_count": len(body_text.split()), "text_sample": body_text[:1200],
                    "internal_links": 0, "external_links": 0}
            for link in page.links:
                target = urlparse(urljoin(final_url, link))
                if target.scheme not in ("http", "https"): continue
                if (target.scheme, target.netloc.lower()) == origin:
                    item["internal_links"] += 1
                    clean = _normalise(target.geturl())
                    if clean not in visited and clean not in queue and len(visited) + len(queue) < max_pages * 4:
                        queue.append(clean)
                else: item["external_links"] += 1
            pages.append(item)
            if delay_seconds: time.sleep(delay_seconds)
        except (HTTPError, URLError, TimeoutError, ValueError, OSError) as exc:
            errors.append({"url": url, "error": str(exc)[:240]})
    title_counts = Counter(page["title"] for page in pages if page["title"])
    findings = []
    for page in pages:
        if page["status"] >= 400: findings.append({"severity":"error","url":page["url"],"issue":f"HTTP status {page['status']}"})
        if not page["title"]: findings.append({"severity":"error","url":page["url"],"issue":"Missing title"})
        elif page["title_length"] > 60: findings.append({"severity":"warning","url":page["url"],"issue":"Title is longer than 60 characters"})
        if page["title"] and title_counts[page["title"]] > 1: findings.append({"severity":"warning","url":page["url"],"issue":"Duplicate title"})
        if not page["description"]: findings.append({"severity":"warning","url":page["url"],"issue":"Missing meta description"})
        elif page["description_length"] > 160: findings.append({"severity":"info","url":page["url"],"issue":"Meta description is longer than 160 characters"})
        if not page["h1"]: findings.append({"severity":"warning","url":page["url"],"issue":"Missing H1 heading"})
        elif len(page["h1"]) > 1: findings.append({"severity":"info","url":page["url"],"issue":"Multiple H1 headings"})
        if page["images_missing_alt"]: findings.append({"severity":"warning","url":page["url"],"issue":f"{page['images_missing_alt']} images missing alt text"})
    summary = {"pages_crawled":len(pages),"errors":sum(row["severity"]=="error" for row in findings),
               "warnings":sum(row["severity"]=="warning" for row in findings),"info":sum(row["severity"]=="info" for row in findings)}
    return {"start_url":root,"pages":pages,"findings":findings,"errors":errors,"summary":summary}
