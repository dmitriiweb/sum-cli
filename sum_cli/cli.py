from argparse import ArgumentParser
from collections import namedtuple

from sum_cli.summarizer import summarize_url

Args = namedtuple("Args", ["url", "model", "language"])


def get_args() -> Args:
    parser = ArgumentParser(
        prog="sum-cli",
        description=(
            "CLI tool to extract and summarize "
            "text from a given URL. Quickly get the key points of any "
            "webpage without reading the full content."
        ),
    )
    parser.add_argument("url", help="URL of the webpage with an article to summarize")
    parser.add_argument(
        "-m",
        "--model",
        default="llama3.2:latest",
        help="Ollama model to use, default is llama3.2:latest",
    )
    parser.add_argument(
        "-l",
        "--language",
        default="english",
        help="Language of the summary, default is english",
    )

    args = parser.parse_args()
    return Args(url=args.url, model=args.model, language=args.language)


def main():
    args = get_args()
    summarize_url(args.url, args.model, args.language)


if __name__ == "__main__":
    main()
