from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)

CHAT_SYSTEM_PROMPT_TEMPLATE = """You are usefull AI assistant.
Use the following context to answer questions.
Be as detailed as possible, but don't make up any information
that's not from the context. If you don't know an answer, say
you don't know. Answers must be in {language}

{context}
"""

chat_output_system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["language", "context"], template=CHAT_SYSTEM_PROMPT_TEMPLATE
    )
)
chat_human_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=["question"], template="{question}")
)
chat_output_messages = [chat_output_system_prompt, chat_human_prompt]
chat_output_chat_template = ChatPromptTemplate(
    input_variables=["language", "context", "question"], messages=chat_output_messages
)

SUM_OUTPUT_SYSTEM_PROMPT_TEMPLATE = """You are an advanced AI model specializing in text summarization. Your task is to generate a concise and informative summary of a given article. Extract the key points while maintaining clarity and coherence. Avoid unnecessary details, opinions, or redundant information.
Output Requirements:
    1. Use {language} for the output.
    2. Keep the summary brief and to the point, ideally within [X] sentences.
    3. Retain the core meaning and key takeaways from the original article.
    4. Use clear and natural language suitable for a general audience.
    5. If the article contains multiple topics, focus on the most important aspects.
"""

SUM_ERROR_SYSTEM_PROMPT_TEMPLATE = """You are an AI assistant specializing in troubleshooting and providing solutions for errors related to text extraction using the newspaper3k Python library.

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

sum_output_system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["language"], template=SUM_OUTPUT_SYSTEM_PROMPT_TEMPLATE
    )
)
sum_error_system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["language"], template=SUM_ERROR_SYSTEM_PROMPT_TEMPLATE
    )
)
sum_human_url_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=["text"], template="{text}")
)
human_error_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=["text"], template="{text}")
)

sum_error_messages = [sum_error_system_prompt, human_error_prompt]
error_chat_template = ChatPromptTemplate(
    input_variables=["language", "text"], messages=sum_error_messages
)
sum_output_messages = [sum_output_system_prompt, sum_human_url_prompt]
sum_output_chat_template = ChatPromptTemplate(
    input_variables=["language", "text"], messages=sum_output_messages
)
