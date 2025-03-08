from dataclasses import dataclass

from newspaper import Article


@dataclass
class ArticleText:
    text: str | None
    error: str | None = None


def get_article_text(url: str) -> ArticleText:
    article = Article(url)
    try:
        article.download()
        article.parse()
    except Exception as e:
        return ArticleText(text=None, error=str(e))

    authors = ", ".join(article.authors)
    try:
        publish_date = article.publish_date.strftime("%B %d, %Y")
    except AttributeError:
        publish_date = ""

    text = f"{article.title}\n\n{publish_date}\n\n{authors}\n\n{article.text}"

    return ArticleText(text=text)
