"""Wikipedia retrieval helpers wrapping the MediaWiki REST API v1."""

import re

import requests
from bs4 import BeautifulSoup

_BASE_URL = "https://en.wikipedia.org/w/rest.php/v1"
_HEADERS = {"User-Agent": "WikipediaQA/1.0"}
_MAX_CONTENT_CHARS = 8_000


def search_pages(query: str, limit: int = 5) -> list[dict]:
    """Search Wikipedia pages and return the raw pages list.

    Args:
        query: Full-text search query string.
        limit: Maximum number of results to return (default 5).

    Returns:
        A list of page dicts (keys: id, key, title, excerpt, description,
        thumbnail), or an empty list on any error or when no results are found.
    """
    url = f"{_BASE_URL}/search/page"
    params: dict[str, str | int] = {"q": query, "limit": limit}
    try:
        response = requests.get(url, params=params, headers=_HEADERS, timeout=10)
        response.raise_for_status()
        data: dict = response.json()
        return data.get("pages") or []
    except (requests.HTTPError, requests.RequestException, ValueError):
        return []


def fetch_page_content(page_key: str) -> str:
    """Fetch a Wikipedia page and return its plain-text content.

    Retrieves the ``with_html`` endpoint, parses the HTML ``html`` field with
    BeautifulSoup, strips all tags, collapses whitespace, and truncates to
    8 000 characters so the result fits comfortably in an LLM context window.

    Args:
        page_key: The normalised page key (e.g. ``"Python_(programming_language)"``).

    Returns:
        Plain-text content string, or an empty string on 404 or any other error.
    """
    url = f"{_BASE_URL}/page/{page_key}/with_html"
    try:
        response = requests.get(url, headers=_HEADERS, timeout=15)
        if response.status_code == 404:
            return ""
        response.raise_for_status()
        data: dict = response.json()
        html: str = data.get("html", "")
        if not html:
            return ""
    except (requests.HTTPError, requests.RequestException, ValueError):
        return ""

    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ")
    # Collapse runs of whitespace (spaces, tabs, newlines) into a single space.
    text = re.sub(r"\s+", " ", text).strip()
    return text[:_MAX_CONTENT_CHARS]
