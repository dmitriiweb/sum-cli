from langchain.schema.document import Document
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


class Embeder:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.embedings = OllamaEmbeddings(model=model_name)
        self.chroma = Chroma(embedding_function=self.embedings)

    def add_texts(self, texts: list[str]):
        self.chroma.add_texts(texts)

    def get_relevant(self, question: str, k: int = 3) -> list[Document]:
        result = self.chroma.similarity_search(question, k=k)
        return result

    def as_retriever(self, k: int = 3):
        return self.chroma.as_retriever(k=k)

    @staticmethod
    def generate_texts(text: str, num_ctx: int) -> list[str]:
        article_words = text.split()
        article_length = len(article_words)
        texts = []
        for i in range(0, article_length, num_ctx):
            texts.append(" ".join(article_words[i : i + num_ctx]))
        return texts
