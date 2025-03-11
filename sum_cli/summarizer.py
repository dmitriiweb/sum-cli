from typing import Any

from langchain.prompts import (
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain_ollama.llms import OllamaLLM

from .get_text_article import get_article_text

OUTPUT_SYSTEM_PROMPT_TEMPLATE = """You are an advanced AI model specializing in text summarization. Your task is to generate a concise and informative summary of a given article. Extract the key points while maintaining clarity and coherence. Avoid unnecessary details, opinions, or redundant information.
Output Requirements:
    1. Use {language} for the output.
    2. Keep the summary brief and to the point, ideally within [X] sentences.
    3. Retain the core meaning and key takeaways from the original article.
    4. Use clear and natural language suitable for a general audience.
    5. If the article contains multiple topics, focus on the most important aspects.
"""

ERROR_SYSTEM_PROMPT_TEMPLATE = """You are an AI assistant specializing in troubleshooting and providing solutions for errors related to text extraction using the newspaper3k Python library.

Task:

    1. Analyze the given error message and understand its cause.
    2. Generate a clear and structured explanation of the error.
    3. Suggest possible solutions to resolve the issue.
    4. Output the response in {language}.

Output Requirements:

    - The response should start with a brief explanation of the error.
    - Provide at least one or more possible solutions, depending on the issue.
    - Use concise and technical language, but make sure the solutions are easy to follow.
    - If additional debugging steps are required, mention them clearly.

Example Input:
Error: "newspaper.article.ArticleException: Article text extraction failed."

Example Output (English):
Error: Article text extraction failed.
Possible Causes:

    - The webpage blocks bots (e.g., requires JavaScript).
    - The URL is incorrect or the page does not exist.
    - The article content is too short for extraction.

Solutions:

    - Try using newspaper.fulltext(html) instead of the default parser.
    - Use requests with a custom User-Agent to fetch the page first.
    - Check if the URL is correct and accessible.
"""

output_system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["language"], template=OUTPUT_SYSTEM_PROMPT_TEMPLATE
    )
)
error_system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["language"], template=ERROR_SYSTEM_PROMPT_TEMPLATE
    )
)
human_url_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=["text"], template="{text}")
)
human_error_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=["text"], template="{text}")
)

error_messages = [error_system_prompt, human_error_prompt]
error_chat_template = ChatPromptTemplate(
    input_variables=["language", "text"], messages=error_messages
)
output_messages = [output_system_prompt, human_url_prompt]
output_chat_template = ChatPromptTemplate(
    input_variables=["language", "text"], messages=output_messages
)



def summarize_url(url: str, model: str, language: str) -> None:
    print("Reading article from URL...", end="\r")
    article = get_article_text(url)
    if article.error is not None:
        _make_output(model, error_chat_template, language, article.error)
        return
    elif article.text is not None:
        _make_output(model, output_chat_template, language, article.text)
        return
    print("Error: Unable to extract text from the provided URL.")
    return


def _make_output(model_name: str, prompt: ChatPromptTemplate, language: str, text: str) -> None:
    model = OllamaLLM(model=model_name)
    chain = prompt | model
    for token in chain.stream({"language": language, "text": text}):
        print(token, end="")
