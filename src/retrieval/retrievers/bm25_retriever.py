from src.document_processing.vector_store import VectorStore
from src.config.settings import settings
from src.document_processing.embeddings import Embedding
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
import numpy as np


class Bm25Retriever:

    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store.get_vector_store()

        self.bm25_retriever = self.build_bm25_from_vectorstore(
            vector_store=self.vector_store,
            k=settings.TOP_K
        )

    def build_bm25_from_vectorstore(
        self,
        vector_store,
        k: int = settings.TOP_K
    ):
        data = vector_store.get(
            include=["documents", "metadatas"]
        )

        documents = [
            Document(
                page_content=text,
                metadata=metadata or {}
            )
            for text, metadata in zip(
                data["documents"],
                data["metadatas"]
            )
        ]

        bm25_retriever = BM25Retriever.from_documents(documents)

        bm25_retriever.k = k

        return bm25_retriever

    def retrieve(self, query: str) -> list[Document]:

        # Same preprocessing used by LangChain BM25
        processed_query = self.bm25_retriever.preprocess_func(query)

        # BM25 scores for all documents
        scores = self.bm25_retriever.vectorizer.get_scores(
            processed_query
        )

        # Sort by BM25 score descending
        top_indices = np.argsort(scores)[::-1][:settings.TOP_K]

        results = []

        for index in top_indices:
            doc = self.bm25_retriever.docs[index]

            doc.metadata["bm25_score"] = float(scores[index])

            results.append(doc)

        return results

    def get_bm25_retriever(self):
        return self.bm25_retriever


if __name__ == "__main__":

    vector_store = VectorStore(
        Embedding().get_embedding_model()
    )

    bm25_retriever = Bm25Retriever(
        vector_store=vector_store
    )

    docs = bm25_retriever.retrieve(
        "What are the common peripheral and central causes of vertigo and dizziness?"
    )

    print(len(docs))
    print("================================")

    for doc in docs:

        print("==========content==============")
        print(doc.page_content)

        print("==========BM25 Score===========")
        print(doc.metadata["bm25_score"])

        print("==========metadata=============")
        print(doc.metadata)

        print("================================")