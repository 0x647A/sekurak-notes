# Flag Search Web Crawler

A Python web crawler built to solve CTF (Capture the Flag) challenges. It recursively explores a target website using breadth-first search to locate a flag matching a configurable regex pattern. The crawler restricts itself to the configured domain over HTTPS, filters out binary files, and applies rate limiting to avoid overloading the target server.

## Table of Contents

- [Description](#description)
- [Requirements](#requirements)
- [Usage](#usage)
- [Features](#features)
- [How It Works](#how-it-works)
- [Sample Output](#sample-output)
- [Notes](#notes)

## Description

The script connects to a configurable `TARGET_URL` and performs a breadth-first traversal of the site, following only links that remain within the same domain over HTTPS. It skips binary files to reduce bandwidth and avoid parsing errors. Links are extracted from standard HTML tags as well as CSS `url()` declarations found in stylesheets and inline styles.

If the crawler encounters text matching the configurable `FLAG_PATTERN` anywhere in a response, it logs the match and terminates immediately.

## Requirements

- Python 3.10 or newer
- Third-party libraries:
  - `requests`
  - `beautifulsoup4`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Run the script directly with Python:

```bash
python3 the_real_scrappy_deal.py
```

Before running, set `TARGET_URL` and `FLAG_PATTERN` at the top of the script to match your target and the expected flag format.

The script logs each visited URL, how many new links were queued, and the discovered flag when found.

## Features

- **Domain-restricted crawling:** Stays within the configured `TARGET_URL` domain over HTTPS.
- **Redirect validation:** Validates the final URL after HTTP redirects to prevent leaving the allowed domain.
- **Text file filtering:** Uses HTTP `HEAD` requests to skip binary files before downloading content.
- **Multi-source URL extraction:** Collects links from `<a>`, `<link>`, `<script>`, and `<img>` tags, and from CSS `url()` declarations.
- **Rate limiting:** Sleeps 1 second between requests to avoid overloading the server.
- **Efficient BFS queue:** Tracks queued URLs separately from visited URLs to prevent duplicate entries in the crawl queue.
- **Pattern detection:** Searches response content using a configurable `FLAG_PATTERN` regex and stops immediately when a match is found.
- **Structured logging:** Uses Python's `logging` module for timestamped, level-aware output.

## How It Works

1. **Initialization:** Starts from `TARGET_URL` and sets up a `requests.Session` with a descriptive `User-Agent`.
2. **Crawling queue:** Maintains a `deque` for breadth-first traversal and a mirrored `set` to prevent duplicate entries.
3. **Validation:** Checks each URL against the configured domain and HTTPS requirement before visiting.
4. **HEAD request:** Sends a lightweight `HEAD` request to check the `Content-Type` header and validate the post-redirect URL.
5. **Content download:** For text resources, fetches the full page and decodes it using the encoding declared in the HTTP response headers.
6. **Pattern search:** Runs `FLAG_PATTERN` against the decoded text content.
7. **Link extraction:** Parses HTML with BeautifulSoup for tag-based links, then applies a CSS `url()` regex for any remaining references.
8. **Queueing:** Adds valid, unqueued URLs to the crawl queue.
9. **Rate limiting:** Waits 1 second after each request cycle.
10. **Termination:** Stops immediately when the flag is found, or when no more URLs remain.

## Sample Output

```
10:42:01 [INFO] Starting crawl: https://example.com/
10:42:01 [INFO] Rate limit: 1 request/s | Pattern: FLAG\{[^}]+\}
10:42:01 [INFO] ------------------------------------------------------------
10:42:01 [INFO] Visiting: https://example.com/
10:42:02 [INFO]   -> Queued 5 new link(s)
10:42:03 [INFO] Visiting: https://example.com/about
10:42:04 [INFO]   -> Queued 2 new link(s)
...
10:42:10 [INFO] Flag found at https://example.com/secret
```

## Notes

- **Scope:** Only URLs within the configured domain and using HTTPS are visited.
- **Binary files:** Images, PDFs, and other non-text resources are skipped after a `HEAD` check.
- **Rate limiting:** The 1-second delay applies per request cycle and helps prevent IP-based blocking.
- **Configuration:** Both `TARGET_URL` and `FLAG_PATTERN` are defined at the top of the script.
- **Error handling:** Network errors are logged as warnings and crawling continues; unexpected errors are logged with a full traceback.
- **CTF context:** This tool is intended for use against systems you are authorized to test, such as CTF challenge environments.
