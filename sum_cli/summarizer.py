from langchain.prompts import (
    ChatPromptTemplate,
)
from langchain_ollama.llms import OllamaLLM

from . import promt_templates as pt
from .get_text_article import get_article_text


def summarize_url(url: str, model: str, language: str) -> None:
    print("Reading article from URL...", end="\r")
    article = get_article_text(url)
    if article.error is not None:
        _make_output(model, pt.error_chat_template, language, article.error)
        return
    elif article.text is not None:
        _make_output(model, pt.output_chat_template, language, article.text)
        return
    print("Error: Unable to extract text from the provided URL.")
    return


def _make_output(
    model_name: str, prompt: ChatPromptTemplate, language: str, text: str
) -> None:
    model = OllamaLLM(model=model_name)
    chain = prompt | model
    for token in chain.stream({"language": language, "text": text}):
        print(token, end="")
