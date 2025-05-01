#!/usr/bin/env python3
import re
import time
import csv
import logging
from collections import deque
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

# ——— CONFIG —————————————————————————————————————————
START_URL = input("Enter site   ").strip()
if not urlparse(START_URL).scheme:
    START_URL = "https://" + START_URL

MAX_PAGES   = 200      # how many pages to visit at most
DELAY       = 1.0      # seconds between requests
OUTPUT_CSV  = "emails.csv"
USER_AGENT  = "EmailScraperBot/1.0"

# ——— LOGGING ———————————————————————————————————————
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger()

# ——— HELPERS ——————————————————————————————————————
EMAIL_RE = re.compile(r"[a-zA-Z0-9.\-+_]+@[a-zA-Z0-9.\-+_]+\.[a-zA-Z]+")

def fetch(url):
    headers = {"User-Agent": USER_AGENT}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        return r.text
    except Exception as ex:
        logger.warning(f"❌ Fetch failed {url}: {ex}")
        return ""

def extract_links(html, base, domain):
    soup = BeautifulSoup(html, "lxml")
    out = set()
    for a in soup.find_all("a", href=True):
        href = urljoin(base, a["href"])
        p = urlparse(href)
        if p.scheme in ("http","https") and p.netloc == domain:
            out.add(p.scheme + "://" + p.netloc + p.path)
    return out

# ——— CRAWL + HARVEST —————————————————————————————————
def crawl_and_harvest(start_url):
    domain = urlparse(start_url).netloc
    queue  = deque([start_url.rstrip("/")])
    seen   = set()
    emails = set()

    while queue and len(seen) < MAX_PAGES:
        url = queue.popleft()
        if url in seen:
            continue

        logger.info(f"Visiting ({len(seen)+1}/{MAX_PAGES}): {url}")
        seen.add(url)

        html = fetch(url)
        # harvest emails
        found = EMAIL_RE.findall(html)
        if found:
            logger.info(f" → Found {len(found)} email(s)")
            emails.update(found)

        # enqueue new internal links
        for link in extract_links(html, url, domain):
            if link not in seen and link not in queue:
                queue.append(link)

        time.sleep(DELAY)

    return emails

# ——— MAIN ————————————————————————————————————————
if __name__ == "__main__":
    logger.info(f"▶️  Starting crawl at {START_URL}")
    all_emails = crawl_and_harvest(START_URL)

    if all_emails:
        logger.info(f"✅ {len(all_emails)} unique emails found.")
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["email"])
            for e in sorted(all_emails):
                writer.writerow([e])
        logger.info(f"📝 Saved to {OUTPUT_CSV}")
    else:
        logger.warning("⚠️ No emails discovered.")
