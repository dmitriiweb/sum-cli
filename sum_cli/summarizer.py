from langchain.prompts import (
    ChatPromptTemplate,
)
from langchain_ollama.llms import OllamaLLM

from . import promt_templates as pt
from .config import SummarizerArgs
from .get_text_article import get_article_text


def summarize_url(args: SummarizerArgs) -> None:
    print("Reading article from URL...", end="\r")
    article = get_article_text(args.url)
    if article.error is not None:
        _make_output(args.model, pt.error_chat_template, args.language, article.error)
        return
    elif article.text is not None:
        _make_output(args.model, pt.output_chat_template, args.language, article.text)
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
