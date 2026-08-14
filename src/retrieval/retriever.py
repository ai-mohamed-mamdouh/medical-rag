from src.retrieval.query import Query
from src.config.settings import settings
from langchain_core.documents import Document
from src.document_processing.vector_store import VectorStore
from src.retrieval.retrievers.bm25_retriever import Bm25Retriever
from src.retrieval.retrievers.vector_retriever import VectorRetriever
from src.retrieval.retrievers.hybrid_retriever import HybridRetriever
from src.retrieval.reranker import Reranker, RerankerModel


class Retriever:

    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

        self.vector_retriever = VectorRetriever(
            vector_store=self.vector_store
        )

        self.bm25_retriever = Bm25Retriever(
            vector_store=self.vector_store
        )

        self.hybrid_retriever = HybridRetriever(
            vector_retriever=self.vector_retriever,
            bm25_retriever=self.bm25_retriever,
            top_k=settings.TOP_K
        )

    def threshold(self, documents : list[Document]) :
        threshold = settings.RELEVANCE_THRESHOLD

        relevant_docs = []
        for doc in documents:
            if doc.metadata['rerank_score'] > threshold :
                relevant_docs.append(doc)

        return relevant_docs
        
    def retrieval_pipeline(self, query: Query, reRanker_model ) -> list[Document]:

        normalized_query = query.normalized_query

        hybrid_docs = self.hybrid_retriever.retrieve(
            query=normalized_query
        )

        reRanker_docs = Reranker(model=reRanker_model).rerank(
            query=query,
            documents=hybrid_docs
            )
        
        relevant_docs = self.threshold(reRanker_docs)

        return relevant_docs





from src.retrieval.query import Query
from src.retrieval.retriever import Retriever
from src.document_processing.embeddings import Embedding
from src.document_processing.vector_store import VectorStore

if __name__ == "__main__":

    vector_store = VectorStore(
        Embedding().get_embedding_model()
    )

    retriever = Retriever(
        vector_store=vector_store
    )

    query = Query(
        original_query=(
            "What are the common peripheral and central causes of vertigo and dizziness?"
        ),
        normalized_query=(
            "What are the common peripheral and central causes of vertigo and dizziness?"
        )
    )

    reRanker_model=RerankerModel().get_reranker_model()

    docs = retriever.retrieval_pipeline(
        query=query,
        reRanker_model=reRanker_model
    )

    for i, doc in enumerate(docs, start=1):
        print(f"Rank: {i}")
        print(doc.page_content)
        print(doc.metadata)
        print("=" * 50)