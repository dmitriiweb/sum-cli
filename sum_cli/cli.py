
from sum_cli.summarizer import summarize_url

from .config import SummarizerArgs


def main():
    args = SummarizerArgs.from_cli()
    summarize_url(args)


if __name__ == "__main__":
    main()
