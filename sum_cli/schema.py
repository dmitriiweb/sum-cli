from __future__ import annotations

from dataclasses import dataclass

import requests
from newspaper import Article

REQUEST_DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Origin": "https://www.google.com",
}


@dataclass
class ArticleText:
    text: str | None
    error: str | None = None

    @classmethod
    def from_url(cls, url: str) -> ArticleText:
        response = requests.get(url, headers=REQUEST_DEFAULT_HEADERS)
        article = Article(url)
        article.set_html(response.text)
        article.parse()
        try:
            article.download()
            article.parse()
        except Exception as e:
            return ArticleText(text=None, error=str(e))

        authors = ", ".join(article.authors)
        try:
            publish_date = article.publish_date.strftime("%B %d, %Y")  # type: ignore
        except AttributeError:
            publish_date = ""

        text = f"{article.title}\n\n{publish_date}\n\n{authors}\n\n{article.text}"

        return ArticleText(text=text)
