from __future__ import annotations

import logging
import re
import time
from collections import deque
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

TARGET_URL = "https://example.com/"
FLAG_PATTERN = r"FLAG\{[^}]+\}"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def is_text_content(headers: dict) -> bool:
    """Return True if Content-Type indicates a text-based resource."""
    content_type = headers.get("content-type", "").lower()
    text_prefixes = (
        "text/",
        "application/javascript",
        "application/json",
        "application/xml",
        "application/xhtml+xml",
    )
    return any(prefix in content_type for prefix in text_prefixes)


def is_valid_url(url: str, target_url: str) -> bool:
    """Return True if *url* belongs to the same HTTPS domain as *target_url*."""
    parsed = urlparse(url)
    target = urlparse(target_url)
    return (
        parsed.scheme == "https"
        and parsed.netloc == target.netloc
        and parsed.port in (None, 443)
    )


def extract_links(content: str, base_url: str) -> set[str]:
    """Extract URLs from HTML and inline CSS content.

    Uses BeautifulSoup for standard HTML tag attributes (<a>, <link>,
    <script>, <img>) and a separate regex pass for CSS ``url()`` declarations
    that tag-based parsing does not cover.
    """
    links: set[str] = set()

    try:
        soup = BeautifulSoup(content, "html.parser")
        for tag, attr in [
            ("a", "href"),
            ("link", "href"),
            ("script", "src"),
            ("img", "src"),
        ]:
            for element in soup.find_all(tag, attrs={attr: True}):
                links.add(urljoin(base_url, element[attr]))
    except Exception as exc:
        logger.debug("HTML parsing failed for %s: %s", base_url, exc)

    # CSS url() references — not captured by tag-based parsing above
    for match in re.finditer(r'url\(["\']?([^"\')\s]+)["\']?\)', content, re.IGNORECASE):
        links.add(urljoin(base_url, match.group(1)))

    return links


# ---------------------------------------------------------------------------
# Crawler
# ---------------------------------------------------------------------------


def search_for_flag() -> str | None:
    """BFS-crawl TARGET_URL and return the first string matching FLAG_PATTERN.

    Returns the flag string if found, or None if the crawl is exhausted.
    """
    visited: set[str] = set()
    queued: set[str] = {TARGET_URL}  # mirrors to_visit; prevents duplicate enqueuing
    to_visit: deque[str] = deque([TARGET_URL])

    session = requests.Session()
    # A semi-transparent User-Agent that identifies this as an automated tool
    # while remaining compatible with servers that reject generic bot strings.
    session.headers["User-Agent"] = "Mozilla/5.0 (compatible; FlagCrawler/1.0)"

    logger.info("Starting crawl: %s", TARGET_URL)
    logger.info("Rate limit: 1 request/s | Pattern: %s", FLAG_PATTERN)
    logger.info("-" * 60)

    while to_visit:
        current_url = to_visit.popleft()

        if current_url in visited:
            continue

        if not is_valid_url(current_url, TARGET_URL):
            continue

        visited.add(current_url)

        try:
            logger.info("Visiting: %s", current_url)

            # HEAD first — avoids downloading binary files unnecessarily
            head = session.head(current_url, timeout=10, allow_redirects=True)

            # Validate the *final* URL after any redirects, not just the original
            if not is_valid_url(head.url, TARGET_URL):
                logger.info("  -> Skipping: redirect leaves domain (%s)", head.url)
                time.sleep(1)
                continue

            if not is_text_content(head.headers):
                logger.info("  -> Skipping: binary content-type")
                time.sleep(1)
                continue

            response = session.get(current_url, timeout=10)
            response.raise_for_status()

            content = response.text

            match = re.search(FLAG_PATTERN, content)
            if match:
                logger.info("Flag found at %s", current_url)
                return match.group(0)

            new_links = extract_links(content, current_url)

            added = 0
            for link in new_links:
                if (
                    link not in visited
                    and link not in queued
                    and is_valid_url(link, TARGET_URL)
                ):
                    to_visit.append(link)
                    queued.add(link)
                    added += 1

            logger.info("  -> Queued %d new link(s)", added)

        except requests.exceptions.RequestException as exc:
            logger.warning("  -> Request failed: %s", exc)
        except Exception as exc:
            logger.error("  -> Unexpected error: %s", exc, exc_info=True)

        time.sleep(1)

    logger.info("Crawl finished. Flag not found.")
    return None


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    flag = search_for_flag()
    if flag:
        print(f"\nResult: {flag}")
    else:
        print("\nFlag not found.")
