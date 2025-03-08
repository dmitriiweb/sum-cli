# sum-cli
CLI tool to extract and summarize text from a given URL. Quickly get the key points of any webpage without reading the full content.

## Requirements
- Ollama
- Python 3.10 or higher

## Installation
```bash
pip install git+https://github.com/dmitriiweb/sum-cli.git
```

## Usage
```bash
sum_cli --help
sum_cli https://example.com
```
## Example
```
$ sum_cli https://python.langchain.com/docs/tutorials/llm_chain/
Here is a concise summary of the article within 10 sentences:

LangChain is a library that enables building applications using language models. This tutorial demonstrates how to build a simple LLM application with LangChain, which translates text from English into another language. The application consists of a single LLM call and prompt templates. Prompt templates take raw user input and return data ready to pass into a language model. A chat template is created with two variables: language and text. The template is used to format the input for the language model. The application invokes the chat model on the formatted prompt, generating a response in the target language. LangSmith provides logging and tracing capabilities, allowing developers to inspect the application's flow. This tutorial covers the basics of using language models, creating prompt templates, and getting observability with LangSmith. For further learning, detailed Conceptual Guides and other resources are available.
```
