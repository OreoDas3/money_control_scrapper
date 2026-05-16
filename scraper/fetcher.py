import logging
import time
import requests
from bs4 import BeautifulSoup


def fetch_page(session, url, config):
    scraper_config = config["scraper"]

    max_retries = scraper_config["max_retries"]
    timeout = scraper_config["timeout"]
    backoff = scraper_config["retry_backoff_seconds"]

    for attempt in range(max_retries):
        try:
            response = session.get(
                url,
                timeout=timeout
            )

            response.raise_for_status()

            return BeautifulSoup(
                response.text,
                "html.parser"
            )

        except requests.RequestException as e:
            logging.warning(
                f"Attempt {attempt + 1}/{max_retries} failed for {url}: {e}"
            )

            if attempt < max_retries - 1:
                sleep_time = backoff * (2 ** attempt)
                time.sleep(sleep_time)

    logging.error(f"Failed after retries: {url}")

    return None