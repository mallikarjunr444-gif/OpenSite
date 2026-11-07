"""Read-only analytics and search connectors for OpenSite.

Credentials are supplied by the user's environment or Streamlit secrets. No
connector sends writes to analytics/search providers.
"""
from datetime import date, datetime, timedelta, timezone
from xml.etree import ElementTree
from typing import Any, Dict, Optional
from urllib.parse import quote

import requests


TIMEOUT = 20


def _request(method: str, url: str, *, token: str = "", headers: Optional[dict] = None, **kwargs):
    request_headers = {"Accept": "application/json", **(headers or {})}
    if token:
        request_headers["Authorization"] = f"Bearer {token}"
    response = requests.request(method, url, headers=request_headers, timeout=TIMEOUT, **kwargs)
    if not response.ok:
        detail = response.text[:300].replace("\n", " ")
        raise RuntimeError(f"Provider returned HTTP {response.status_code}: {detail}")
    return response.json()


def search_console_report(access_token: str, property_url: str, days: int = 28) -> Dict[str, Any]:
    end = date.today() - timedelta(days=3)  # Search Console data is delayed.
    start = end - timedelta(days=days - 1)
    url = f"https://www.googleapis.com/webmasters/v3/sites/{quote(property_url, safe='')}/searchAnalytics/query"
    body = {"startDate": start.isoformat(), "endDate": end.isoformat(), "dimensions": ["date"], "rowLimit": 25000, "dataState": "final"}
    rows = _request("POST", url, token=access_token, json=body).get("rows", [])
    return {"provider": "Google Search Console", "range": f"{start} – {end}", "rows": rows,
            "clicks": sum(row.get("clicks", 0) for row in rows),
            "impressions": sum(row.get("impressions", 0) for row in rows),
            "ctr": (sum(row.get("clicks", 0) for row in rows) / sum(row.get("impressions", 0) for row in rows)) if rows and sum(row.get("impressions", 0) for row in rows) else 0,
            "average_position": (sum(row.get("position", 0) * row.get("impressions", 0) for row in rows) / sum(row.get("impressions", 0) for row in rows)) if rows and sum(row.get("impressions", 0) for row in rows) else None}


def search_console_queries(access_token: str, property_url: str, days: int = 28) -> Dict[str, Any]:
    end = date.today() - timedelta(days=3)
    start = end - timedelta(days=days - 1)
    url = f"https://www.googleapis.com/webmasters/v3/sites/{quote(property_url, safe='')}/searchAnalytics/query"
    body = {"startDate":start.isoformat(),"endDate":end.isoformat(),"dimensions":["query"],"rowLimit":1000,"dataState":"final"}
    rows = _request("POST",url,token=access_token,json=body).get("rows",[])
    return {"provider":"Google Search Console","range":f"{start} – {end}","rows":[{"query":row.get("keys",[""])[0],"clicks":row.get("clicks",0),"impressions":row.get("impressions",0),"ctr":row.get("ctr",0),"position":row.get("position",0)} for row in rows]}


def ga4_report(access_token: str, property_id: str, days: int = 28) -> Dict[str, Any]:
    url = f"https://analyticsdata.googleapis.com/v1beta/properties/{quote(property_id, safe='')}:runReport"
    body = {"dateRanges": [{"startDate": f"{days}daysAgo", "endDate": "yesterday"}],
            "metrics": [{"name": "sessions"}, {"name": "totalUsers"}, {"name": "conversions"}, {"name": "sessionConversionRate"}],
            "dimensions": [{"name": "date"}], "orderBys": [{"dimension": {"dimensionName": "date"}}], "limit": 1000}
    payload = _request("POST", url, token=access_token, json=body)
    rows = []
    for row in payload.get("rows", []):
        values = [value.get("value") for value in row.get("metricValues", [])]
        rows.append({"date": row.get("dimensionValues", [{}])[0].get("value", ""), "sessions": values[0] if len(values)>0 else "0", "users": values[1] if len(values)>1 else "0", "conversions": values[2] if len(values)>2 else "0", "conversion_rate": values[3] if len(values)>3 else "0"})
    return {"provider": "Google Analytics 4", "rows": rows, "sessions": sum(int(row["sessions"]) for row in rows), "users": sum(int(row["users"]) for row in rows), "conversions": sum(float(row["conversions"]) for row in rows)}


def plausible_report(api_key: str, domain: str, base_url: str = "https://plausible.io", period: str = "30d") -> Dict[str, Any]:
    base_url = base_url.rstrip("/")
    headers = {"Authorization": f"Bearer {api_key}"}
    url = f"{base_url}/api/v2/query"
    body = {"site_id": domain, "metrics": ["visitors", "visits", "pageviews", "bounce_rate", "visit_duration"], "date_range": period}
    return {"provider": "Plausible Analytics", **_request("POST", url, headers=headers, json={"query": body})}


def posthog_report(api_key: str, project_id: str, host: str = "https://us.posthog.com") -> Dict[str, Any]:
    url = f"{host.rstrip('/')}/api/projects/{quote(project_id, safe='')}/query"
    query = "SELECT toDate(timestamp) AS day, count() AS events, count(DISTINCT distinct_id) AS users FROM events WHERE timestamp >= now() - INTERVAL 30 DAY GROUP BY day ORDER BY day"
    payload = _request("POST", url, token=api_key, json={"query": {"kind": "HogQLQuery", "query": query}, "name": "OpenSite 30 day event trend"})
    return {"provider": "PostHog", "columns": payload.get("columns", []), "rows": payload.get("results", [])}


def umami_report(api_key: str, website_id: str, base_url: str = "https://api.umami.is/v1") -> Dict[str, Any]:
    now = datetime.now(timezone.utc)
    start = int((now - timedelta(days=30)).timestamp() * 1000)
    end = int(now.timestamp() * 1000)
    url = f"{base_url.rstrip('/')}/websites/{quote(website_id, safe='')}/stats"
    return {"provider": "Umami", **_request("GET", url, token=api_key, params={"startAt": start, "endAt": end})}


def matomo_report(base_url: str, site_id: str, token_auth: str) -> Dict[str, Any]:
    url = f"{base_url.rstrip('/')}/index.php"
    payload = _request("GET", url, params={"module": "API", "method": "VisitsSummary.get", "idSite": site_id,
                                           "date": "last30", "period": "day", "format": "JSON", "token_auth": token_auth})
    if isinstance(payload, dict) and payload.get("result") == "error":
        raise RuntimeError(payload.get("message", "Matomo API error"))
    return {"provider": "Matomo", "results": payload}


def pagespeed_report(url: str, strategy: str = "mobile") -> Dict[str, Any]:
    endpoint = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    payload = _request("GET", endpoint, params={"url": url, "strategy": strategy, "category": ["performance", "seo", "accessibility"]})
    categories = payload.get("lighthouseResult", {}).get("categories", {})
    return {"provider": "Google PageSpeed Insights", "url": url, "strategy": strategy,
            "scores": {name: round((item.get("score") or 0) * 100) for name, item in categories.items()},
            "audits": payload.get("lighthouseResult", {}).get("audits", {})}


def crux_report(api_key: str, url: str) -> Dict[str, Any]:
    endpoint="https://chromeuxreport.googleapis.com/v1/records:queryRecord"
    payload=_request("POST",endpoint,params={"key":api_key},json={"url":url})
    record=payload.get("record",{})
    return {"provider":"Chrome UX Report","url":url,"collection_period":record.get("collectionPeriod",{}),"metrics":record.get("metrics",{})}


def serp_bear_keywords(base_url: str, api_key: str, domain: str) -> Dict[str, Any]:
    url=f"{base_url.rstrip('/')}/api/keywords"
    payload=_request("GET",url,token=api_key,params={"domain":domain})
    return {"provider":"SerpBear","keywords":payload.get("keywords",[])}


def growthbook_experiments(base_url: str, api_key: str) -> Dict[str, Any]:
    url=f"{base_url.rstrip('/')}/api/v1/experiments"
    payload=_request("GET",url,token=api_key)
    return {"provider":"GrowthBook","experiments":payload.get("experiments",[])}


def google_search_updates(limit: int = 20) -> Dict[str, Any]:
    """Fetch recent notices from Google's official Search Central RSS feed."""
    url="https://feeds.feedburner.com/blogspot/amDG"
    response=requests.get(url,headers={"User-Agent":"OpenSite/1.0 (Search Central update reader)"},timeout=TIMEOUT)
    if not response.ok: raise RuntimeError(f"Google Search Central feed returned HTTP {response.status_code}")
    root=ElementTree.fromstring(response.content)
    entries=[]
    for item in root.findall(".//item")[:limit]:
        entries.append({"title":item.findtext("title",default="").strip(),"url":item.findtext("link",default="").strip(),
                        "published":item.findtext("pubDate",default="").strip(),"summary":item.findtext("description",default="").strip()})
    return {"provider":"Google Search Central","updates":entries}
