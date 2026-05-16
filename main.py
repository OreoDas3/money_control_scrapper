import pandas as pd
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from common.config import load_config
from common.logger import setup_logger
from common.session_manager import create_session

from scraper.link_extractor import get_business_links
from scraper.article_parser import scrape_article

from loader.snowflake_loader import load_to_snowflake


def main():
    # Load config
    config = load_config()

    # Setup logger
    setup_logger(config)

    logging.info("Starting Moneycontrol scraper pipeline")

    # Create reusable session
    session = create_session(config)

    # Fetch business article links
    links = get_business_links(session, config)

    if not links:
        logging.warning("No article links found")
        return

    logging.info(f"Total article links found: {len(links)}")

    all_articles = []

    # Parallel scraping
    with ThreadPoolExecutor(
        max_workers=config["scraper"]["thread_pool_size"]
    ) as executor:

        futures = [
            executor.submit(scrape_article, session, link, config)
            for link in links
        ]

        for future in as_completed(futures):
            try:
                article = future.result()

                if article:
                    all_articles.append(article.to_dict())

            except Exception as e:
                logging.error(f"Thread execution failed: {e}")

    if not all_articles:
        logging.warning("No articles scraped successfully")
        return

    df = pd.DataFrame(all_articles)

    logging.info(f"Total scraped rows: {len(df)}")

    # Load into Snowflake
    load_to_snowflake(df, config)

    logging.info("Pipeline execution completed successfully")


if __name__ == "__main__":
    main()