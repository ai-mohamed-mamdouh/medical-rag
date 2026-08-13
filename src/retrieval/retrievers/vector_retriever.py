from src.document_processing.vector_store import VectorStore
from src.config.settings import settings
from src.document_processing.embeddings import Embedding


class VectorRetriever:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store.get_vector_store()

    def retrieve(self, query: str):
        results = self.vector_store.similarity_search_with_relevance_scores(
            query=query,
            k=settings.TOP_K
        )

        documents = []

        for doc, score in results:
            doc.metadata["similarity_score"] = score
            documents.append(doc)

        return documents


if __name__ == "__main__":
    vector_store = VectorStore(
        Embedding().get_embedding_model()
    )

    vector_retriever = VectorRetriever(
        vector_store=vector_store
    )

    docs = vector_retriever.retrieve(
        "What are the common peripheral and central causes of vertigo and dizziness?"
    )

    print(len(docs))
    print("================================")

    for doc in docs:
        print("==========content==============")
        print(doc.page_content)

        print("==========metadata=============")
        print(doc.metadata)

        print("================================")