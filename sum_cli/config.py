from __future__ import annotations

from argparse import ArgumentParser
from dataclasses import dataclass


@dataclass
class SummarizerArgs:
    url: str
    model: str
    language: str
    embeding_name: str
    is_chat: bool
    num_ctx: int

    @classmethod
    def from_cli(cls) -> SummarizerArgs:
        parser = ArgumentParser(
            prog="sum-cli",
            description=(
                "CLI tool to extract and summarize "
                "text from a given URL. Quickly get the key points of any "
                "webpage without reading the full content."
            ),
        )
        parser.add_argument(
            "url", help="URL of the webpage with an article to summarize"
        )
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
        parser.add_argument(
            "-c",
            "--chat",
            action="store_true",
            help="After summarizing, chat with the model",
        )
        parser.add_argument(
            "-e",
            "--embeding",
            default="nomic-embed-text:latest",
            help="Embeding model to use, default is nomic-embed-text:latest",
        )
        parser.add_argument(
            "-n",
            "--num_ctx",
            default=8192,
            type=int,
            help="Number of context tokens for the embeding model, default is 8192",
        )

        args = parser.parse_args()
        return SummarizerArgs(
            url=args.url,
            model=args.model,
            language=args.language,
            embeding_name=args.embeding,
            is_chat=args.chat,
            num_ctx=args.num_ctx,
        )
