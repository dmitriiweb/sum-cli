import sys

from langchain_core.output_parsers import StrOutputParser
from langchain_ollama.chat_models import ChatOllama

from . import embedings as emb
from . import promt_templates as pt
from . import schema
from .config import SummarizerArgs


class ChatSummarizerError(Exception): ...


def summarize_url(args: SummarizerArgs) -> None:
    print("Reading article from URL...", end="\r")
    article = schema.ArticleText.from_url(args.url)
    if article.error is not None:
        prompt = pt.error_chat_template
        text = article.error
    elif article.text is not None:
        prompt = pt.sum_output_chat_template
        text = article.text
    else:
        print("Error: Unable to extract text from the provided URL.")
        return
    model = ChatOllama(model=args.model)
    chain = prompt | model
    for token in chain.stream({"language": args.language, "text": text}):
        print(token.content, end="")
    if not args.is_chat:
        return
    try:
        _chat(args, article)
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)


def _chat(args: SummarizerArgs, article: schema.ArticleText):
    if article.text is None:
        raise ChatSummarizerError("No text to chat with")

    article_words = article.text.split()
    article_length = len(article_words)
    use_embedings = False
    if article_length > args.num_ctx:
        texts = emb.Embeder.generate_texts(article.text, args.num_ctx)
        embeder = emb.Embeder(args.embeding_name)
        print("\n\nGenerating embeddings...\n\n")
        embeder.add_texts(texts)
        use_embedings = True
    model = ChatOllama(model=args.model)
    chat_chain = pt.chat_output_chat_template | model | StrOutputParser()
    while True:
        question = input("\n\nYou: ")
        if use_embedings:
            context = "\n\n".join([str(i) for i in embeder.get_relevant(question)])
        else:
            context = article.text
        for token in chat_chain.stream(
            {"context": context, "question": question, "language": args.language}
        ):
            print(token, end="")
        print()
