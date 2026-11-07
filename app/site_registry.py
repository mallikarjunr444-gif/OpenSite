"""Local registry of user properties added in the OpenSite UI."""
import json
import re
from pathlib import Path
from urllib.parse import urlparse

from app.config import settings


def registry_path():
    return Path(settings.OPENSITE_SITES_PATH).expanduser() if settings.OPENSITE_SITES_PATH else Path(__file__).resolve().parent / "data" / "sites.json"


def load_custom_sites():
    try:
        data=json.loads(registry_path().read_text(encoding="utf-8"))
        return data if isinstance(data,list) else []
    except (OSError,json.JSONDecodeError):
        return []


def add_site(value):
    raw=value.strip()
    parsed=urlparse(raw if "://" in raw else f"https://{raw}")
    if parsed.scheme not in ("http","https") or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Enter a valid public website domain or URL.")
    if parsed.hostname == "localhost" or "." not in parsed.hostname:
        raise ValueError("Enter a public domain name.")
    domain=parsed.hostname.lower()
    slug=re.sub(r"[^a-z0-9]+","_",domain).strip("_") or "site"
    site_id=f"site_{slug}"
    sites=load_custom_sites()
    if any(site.get("site_id")==site_id for site in sites): return site_id
    sites.append({"site_id":site_id,"domain":domain,"title":domain,"niche":"","baseline_monthly_organic":0,"baseline_conversion_rate":"—","history":[]})
    path=registry_path(); path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix(".tmp"); temp.write_text(json.dumps(sites,indent=2),encoding="utf-8"); temp.replace(path)
    return site_id
