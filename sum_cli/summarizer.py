from .get_text_article import get_article_text


def summarize_url(url: str, model: str, language: str):
    print(f"{url=}")
    print()
    article_text = get_article_text(url)
    print(article_text.text)
