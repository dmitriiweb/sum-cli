from langchain_ollama.llms import OllamaLLM

from . import promt_templates as pt
from .config import SummarizerArgs
from .get_text_article import get_article_text


def summarize_url(args: SummarizerArgs) -> None:
    print("Reading article from URL...", end="\r")
    article = get_article_text(args.url)
    if article.error is not None:
        prompt = pt.error_chat_template
        text = article.error
    elif article.text is not None:
        prompt = pt.output_chat_template
        text = article.text
    else:
        print("Error: Unable to extract text from the provided URL.")
        return
    model = OllamaLLM(model=args.model)
    chain = prompt | model
    for token in chain.stream({"language": args.language, "text": text}):
        print(token, end="")
