from __future__ import annotations

import os
import re
from datetime import datetime, timedelta, timezone
from typing import List
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from ..sample_data import DEFAULT_ARTICLES, SAMPLE_ARTICLES


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def _normalize_topic(topic: str) -> str:
    topic = topic.strip().lower()
    aliases = {
        "ai": "artificial intelligence",
        "artificial intelligence": "artificial intelligence",
        "petrol": "petrol",
        "oil": "petrol",
        "energy": "petrol",
        "war": "war",
        "conflict": "war",
        "technology": "technology",
        "tech": "technology",
        "finance": "finance",
    }
    return aliases.get(topic, topic)


def _filter_articles_by_timeframe(articles: List[dict], timeframe: str) -> List[dict]:
    now = datetime.now(timezone.utc)
    days = {"daily": 1, "weekly": 7, "monthly": 30}.get(timeframe, 7)
    cutoff = now - timedelta(days=days)

    out = []
    for art in articles:
        try:
            published = datetime.fromisoformat((art.get("published_at") or "").replace("Z", "+00:00"))
            if published >= cutoff:
                out.append(art)
        except Exception:
            out.append(art)
    return out or articles


def _scrape_google_news_rss(topic: str, timeframe: str, region: str) -> List[dict]:
    query = re.sub(r"\s+", "+", topic.strip())
    hl = "en-IN" if region.lower() == "india" else "en-US"
    gl = "IN" if region.lower() == "india" else "US"
    ceid = f"{gl}:{hl}"
    rss_url = f"https://news.google.com/rss/search?q={query}&hl={hl}&gl={gl}&ceid={ceid}"
    try:
        res = requests.get(rss_url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "xml")
        items = []
        for item in soup.find_all("item")[:8]:
            link = item.link.text.strip() if item.link else "#"
            title = item.title.text.strip() if item.title else ""
            source_tag = item.find("source")
            source = source_tag.text.strip() if source_tag else urlparse(link).netloc
            pub = item.pubDate.text.strip() if item.pubDate else ""
            items.append(
                {
                    "title": title,
                    "source": source or "Google News",
                    "published_at": pub,
                    "description": item.description.text.strip() if item.description else "",
                    "url": link,
                }
            )
        return items
    except Exception:
        return []


def _fetch_newsapi(topic: str, region: str, timeframe: str) -> List[dict]:
    key = os.getenv("NEWSAPI_KEY", "").strip()
    if not key:
        return []

    from_date = {
        "daily": (datetime.utcnow() - timedelta(days=1)).date().isoformat(),
        "weekly": (datetime.utcnow() - timedelta(days=7)).date().isoformat(),
        "monthly": (datetime.utcnow() - timedelta(days=30)).date().isoformat(),
    }.get(timeframe, (datetime.utcnow() - timedelta(days=7)).date().isoformat())

    params = {
        "q": topic,
        "from": from_date,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 8,
        "apiKey": key,
    }
    if region and region.lower() not in {"global", "all"}:
        params["country"] = region.lower()[:2]

    url = "https://newsapi.org/v2/everything"
    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()
        articles = []
        for item in data.get("articles", [])[:8]:
            articles.append(
                {
                    "title": item.get("title") or "",
                    "source": (item.get("source") or {}).get("name") or "Unknown",
                    "published_at": item.get("publishedAt") or "",
                    "description": item.get("description") or item.get("content") or "",
                    "url": item.get("url") or "#",
                }
            )
        return articles
    except Exception:
        return []


def _fetch_gnews(topic: str, region: str, timeframe: str) -> List[dict]:
    key = os.getenv("GNEWS_KEY", "").strip()
    if not key:
        return []

    from_date = {
        "daily": (datetime.utcnow() - timedelta(days=1)).date().isoformat(),
        "weekly": (datetime.utcnow() - timedelta(days=7)).date().isoformat(),
        "monthly": (datetime.utcnow() - timedelta(days=30)).date().isoformat(),
    }.get(timeframe, (datetime.utcnow() - timedelta(days=7)).date().isoformat())

    url = "https://gnews.io/api/v4/search"
    params = {
        "q": topic,
        "lang": "en",
        "max": 8,
        "token": key,
        "from": from_date,
    }
    if region and region.lower() not in {"global", "all"}:
        params["country"] = region.lower()[:2]

    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()
        articles = []
        for item in data.get("articles", [])[:8]:
            articles.append(
                {
                    "title": item.get("title") or "",
                    "source": (item.get("source") or {}).get("name") or "Unknown",
                    "published_at": item.get("publishedAt") or "",
                    "description": item.get("description") or item.get("content") or "",
                    "url": item.get("url") or "#",
                }
            )
        return articles
    except Exception:
        return []


def _extract_page_text(html_text: str) -> str:
    soup = BeautifulSoup(html_text, "html.parser")

    for tag in soup(["script", "style", "noscript", "iframe", "svg"]):
        tag.decompose()

    candidates = []
    # Prefer article/main bodies
    for selector in ["article", "main", "[role='main']"]:
        for el in soup.select(selector):
            texts = [p.get_text(" ", strip=True) for p in el.find_all(["p", "h1", "h2", "h3", "li"]) ]
            joined = "\n".join(t for t in texts if len(t.split()) > 3)
            if len(joined.split()) > 80:
                candidates.append(joined)

    # Meta descriptions if page body is thin
    meta_desc = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        meta_desc = meta.get("content", "").strip()
    og = soup.find("meta", attrs={"property": "og:description"})
    if og and og.get("content"):
        meta_desc = max(meta_desc, og.get("content", "").strip(), key=len) if meta_desc else og.get("content", "").strip()

    # Fallback: collect paragraphs
    if not candidates:
        paras = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
        paras = [p for p in paras if len(p.split()) > 5]
        if paras:
            candidates.append("\n".join(paras[:25]))

    best = max(candidates, key=lambda s: len(s), default="")
    if len(best.split()) < 60 and meta_desc:
        best = (best + "\n" + meta_desc).strip()

    return re.sub(r"\n{3,}", "\n\n", best).strip()


def _fetch_article_page(url: str) -> str:
    if not url or url == "#":
        return ""
    try:
        res = requests.get(url, headers=HEADERS, timeout=12, allow_redirects=True)
        res.raise_for_status()
        ctype = res.headers.get("content-type", "").lower()
        if "text/html" not in ctype and "application/xhtml" not in ctype:
            return ""
        return _extract_page_text(res.text)
    except Exception:
        return ""


def _enrich_with_full_pages(articles: List[dict]) -> List[dict]:
    enriched = []
    for art in articles:
        full_text = _fetch_article_page(art.get("url", ""))
        if full_text:
            art = dict(art)
            art["full_text"] = full_text
        enriched.append(art)
    return enriched


def get_articles(topic: str, timeframe: str, region: str) -> List[dict]:
    normalized = _normalize_topic(topic)

    articles = _fetch_newsapi(normalized, region, timeframe)
    if not articles:
        articles = _fetch_gnews(normalized, region, timeframe)
    if not articles:
        articles = _scrape_google_news_rss(normalized, timeframe, region)
    if not articles:
        articles = list(SAMPLE_ARTICLES.get(normalized, DEFAULT_ARTICLES))

    articles = _filter_articles_by_timeframe(articles, timeframe)
    articles = _enrich_with_full_pages(articles[:8])
    return articles[:8]
