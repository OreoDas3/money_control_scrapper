import logging


def setup_logger(config):
    log_level = config["logging"]["level"].upper()

    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s - %(levelname)s - %(message)s"
    )