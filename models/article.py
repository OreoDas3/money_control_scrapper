from dataclasses import dataclass


@dataclass
class Article:
    title: str
    author: str
    publication_date: str
    article_url: str
    content: str

    def to_dict(self):
        return {
            "TITLE": self.title,
            "AUTHOR": self.author,
            "PUBLICATION_DATE": self.publication_date,
            "ARTICLE_URL": self.article_url,
            "CONTENT": self.content
        }