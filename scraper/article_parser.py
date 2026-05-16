from models.article import Article
from scraper.fetcher import fetch_page


def extract_title(soup):
    title_selectors = [
        ("h1", "maintext"),
        ("h1", None)
    ]

    for tag, cls in title_selectors:
        elem = soup.find(tag, class_=cls) if cls else soup.find(tag)

        if elem:
            title = elem.get_text(" ", strip=True)

            if title:
                return title

    og_title = soup.find(
        "meta",
        attrs={"property": "og:title"}
    )

    if og_title:
        title = og_title.get("content")

        if title:
            return title

    if soup.title:
        return soup.title.get_text(strip=True)

    return None


def extract_author(soup):
    authors = []

    disclaimer_text = ""

    disclaimer_div = soup.find("div", class_="disclaimer")

    if disclaimer_div:
        disclaimer_text += disclaimer_div.get_text(
            " ",
            strip=True
        ).lower()

    disclaimer_em = soup.find("em")

    if disclaimer_em:
        disclaimer_text += " " + disclaimer_em.get_text(
            " ",
            strip=True
        ).lower()

    if disclaimer_text:
        if "external partner" in disclaimer_text:
            return "External Source"

        if "experts on moneycontrol.com" in disclaimer_text:
            return "Moneycontrol Experts"

    selector_paths = [
        ("div", "left_block", "div", "article_author"),
        ("div", None, "div", "article_author"),
    ]

    for parent_tag, parent_cls, child_tag, child_cls in selector_paths:
        parent = (
            soup.find(parent_tag, class_=parent_cls)
            if parent_cls else soup
        )

        if parent:
            author_div = parent.find(
                child_tag,
                class_=child_cls
            )

            if author_div:
                author_links = author_div.find_all("a")

                if author_links:
                    for link in author_links:
                        name = (
                            link.get("title")
                            or link.get_text(strip=True)
                        )

                        if name:
                            authors.append(name)

                else:
                    plain_author = author_div.get_text(
                        " ",
                        strip=True
                    )

                    if plain_author:
                        authors.append(plain_author)

                if authors:
                    return ", ".join(dict.fromkeys(authors))

    author_links = soup.find_all("a", rel="author")

    for link in author_links:
        name = link.get_text(strip=True)

        if name:
            authors.append(name)

    if authors:
        return ", ".join(dict.fromkeys(authors))

    meta_author = soup.find(
        "meta",
        attrs={"name": "author"}
    )

    if meta_author:
        meta_name = meta_author.get("content")

        if meta_name:
            authors.append(meta_name)

    if authors:
        return ", ".join(dict.fromkeys(authors))

    fallback_classes = [
        "author_name",
        "auth_name"
    ]

    for cls in fallback_classes:
        elem = soup.find(class_=cls)

        if elem:
            name = elem.get_text(" ", strip=True)

            if name:
                return name

    return None


def extract_publication_date(soup):
    selector_strategies = [
        {
            "parent_tag": "div",
            "parent_class": "left_block",
            "child_tag": "div",
            "child_class": "article_schedule"
        },
        {
            "parent_tag": "h1",
            "parent_class": "maintext",
            "child_tag": "p",
            "child_class": None
        }
    ]

    for strategy in selector_strategies:
        parent = soup.find(
            strategy["parent_tag"],
            class_=strategy["parent_class"]
        )

        if parent:
            if strategy["child_class"]:
                child = parent.find(
                    strategy["child_tag"],
                    class_=strategy["child_class"]
                )
            else:
                child = parent.find(
                    strategy["child_tag"]
                )

            if child:
                value = child.get_text(
                    " ",
                    strip=True
                )

                if value:
                    return value

    timedate_div = soup.find(
        "div",
        class_=lambda cls: cls and "timedate_share" in cls
    )

    if timedate_div:
        date_p = timedate_div.find("p")

        if date_p:
            value = date_p.get_text(" ", strip=True)

            if value:
                return value

    meta_date = soup.find(
        "meta",
        attrs={"property": "article:published_time"}
    )

    if meta_date:
        value = meta_date.get("content")

        if value:
            return value

    fallback_classes = [
        "article_schedule",
        "published_datetime",
        "date"
    ]

    for cls in fallback_classes:
        elem = soup.find(class_=cls)

        if elem:
            value = elem.get_text(" ", strip=True)

            if value:
                return value

    return None


def extract_content(soup):
    content_parts = []
    seen = set()

    junk_patterns = [
        "My Account Follow us on:",
        "Advertisement",
        "Read more",
        "Follow us on",
        "Subscribe",
        "Login",
        "Sign in",
        "WhatsApp",
        "Telegram",
        "Trending",
        "Recommended Stories",
        "First Published",
        "Updated:",
        "Business News",
        "Click here",
        "Join Us",
        "Share:",
    ]

    def is_valid_text(text):
        if not text:
            return False

        if len(text) < 30:
            return False

        if any(junk in text for junk in junk_patterns):
            return False

        return True

    fintech_wrapper = soup.find(
        "section",
        id="fintech_wrapper"
    )

    if fintech_wrapper:
        page_left = fintech_wrapper.find(
            "div",
            class_=lambda x: x and "page_left_wrapper" in x
        )

        if page_left:
            fintech_paragraphs = page_left.find_all(
                "p",
                class_=lambda x: x and "fintech_content_block" in x
            )

            for p in fintech_paragraphs:
                text = p.get_text(" ", strip=True)

                if is_valid_text(text) and text not in seen:
                    seen.add(text)
                    content_parts.append(text)

            summary_div = page_left.find(
                "div",
                class_="fintech_summary"
            )

            if summary_div:
                summary_text = summary_div.get_text(
                    " ",
                    strip=True
                )

                if is_valid_text(summary_text):
                    content_parts.append(summary_text)

            if content_parts:
                return " ".join(content_parts)

    content_strategies = [
        "content_wrapper",
        "article_content",
        "contentSec",
        "page_left_wrapper",
        "disBdy",
    ]

    for cls in content_strategies:
        container = soup.find(
            class_=lambda x: x and cls in x
        )

        if not container:
            continue

        paragraphs = container.find_all("p")

        for p in paragraphs:
            text = p.get_text(" ", strip=True)

            if is_valid_text(text) and text not in seen:
                seen.add(text)
                content_parts.append(text)

        if content_parts:
            return " ".join(content_parts)

    for p in soup.find_all("p"):
        text = p.get_text(" ", strip=True)

        if is_valid_text(text) and text not in seen:
            seen.add(text)
            content_parts.append(text)

    return " ".join(content_parts) if content_parts else None


def scrape_article(session, url, config):
    soup = fetch_page(session, url, config)

    if not soup:
        return None

    return Article(
        title=extract_title(soup),
        author=extract_author(soup),
        publication_date=extract_publication_date(soup),
        article_url=url,
        content=extract_content(soup)
    )