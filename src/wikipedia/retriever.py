"""Wikipedia retrieval helpers wrapping the MediaWiki REST API v1."""

import re
import time

import requests
from bs4 import BeautifulSoup

_BASE_URL = "https://en.wikipedia.org/w/rest.php/v1"
_HEADERS = {"User-Agent": "WikipediaQA/1.0"}
_MAX_CONTENT_CHARS = 8_000
_SEARCH_RETRIES = 2
_FETCH_RETRIES = 2
_RETRY_DELAY = 1.5  # seconds between retries on empty/failed responses


def search_pages(query: str, limit: int = 5) -> list[dict]:
    """Search Wikipedia pages and return the raw pages list.

    Retries up to _SEARCH_RETRIES times if the API returns an empty result set,
    which can happen under transient load. Returns [] on persistent failure.
    """
    url = f"{_BASE_URL}/search/page"
    params: dict[str, str | int] = {"q": query, "limit": limit}

    for attempt in range(_SEARCH_RETRIES + 1):
        try:
            response = requests.get(url, params=params, headers=_HEADERS, timeout=10)
            response.raise_for_status()
            pages = response.json().get("pages") or []
            if pages or attempt == _SEARCH_RETRIES:
                return pages
            # Empty result on non-final attempt — retry after a short delay
            time.sleep(_RETRY_DELAY)
        except (requests.HTTPError, requests.RequestException, ValueError):
            if attempt < _SEARCH_RETRIES:
                time.sleep(_RETRY_DELAY)
            else:
                return []

    return []


def fetch_page_content(page_key: str) -> str:
    """Fetch a Wikipedia page and return its plain-text content.

    Retries up to _FETCH_RETRIES times on empty content or transient errors,
    which can occur when the Wikipedia API is under load.

    Returns plain-text content truncated to _MAX_CONTENT_CHARS, or "" on
    persistent failure or 404.
    """
    url = f"{_BASE_URL}/page/{page_key}/with_html"

    for attempt in range(_FETCH_RETRIES + 1):
        try:
            response = requests.get(url, headers=_HEADERS, timeout=15)
            if response.status_code == 404:
                return ""
            response.raise_for_status()
            html: str = response.json().get("html", "")
            if html:
                soup = BeautifulSoup(html, "html.parser")
                text = soup.get_text(separator=" ")
                text = re.sub(r"\s+", " ", text).strip()
                if text:
                    return text[:_MAX_CONTENT_CHARS]
            # Empty content — retry unless this is the last attempt
            if attempt < _FETCH_RETRIES:
                time.sleep(_RETRY_DELAY)
        except (requests.HTTPError, requests.RequestException, ValueError):
            if attempt < _FETCH_RETRIES:
                time.sleep(_RETRY_DELAY)
            else:
                return ""

    return ""
