import requests


def create_session(config):
    session = requests.Session()

    headers = {
        "User-Agent": config["headers"]["user_agent"],
        "Accept-Language": config["headers"]["accept_language"]
    }

    session.headers.update(headers)

    return session