import logging
import re
from urllib.parse import urlparse, urlunparse

from scraper.fetcher import fetch_page


def normalize_url(url):
    parsed = urlparse(url)

    return urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        "",
        "",
        ""
    ))


def get_business_links(session, config):
    homepage_url = config["scraper"]["homepage_url"]
    article_pattern = re.compile(config["patterns"]["article_regex"])

    soup = fetch_page(session, homepage_url, config)

    if not soup:
        return []

    links = set()

    for a in soup.find_all("a", href=True):
        raw_href = a["href"]

        if not raw_href.startswith("https"):
            continue

        href = normalize_url(raw_href)

        if article_pattern.match(href):
            links.add(href)

    logging.info(f"Filtered business article links: {len(links)}")

    return list(links)