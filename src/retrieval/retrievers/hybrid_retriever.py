from langchain_core.documents import Document
from src.retrieval.retrievers.rrf_fusion import RRFFusion
from src.config.settings import settings

class HybridRetriever:

    def __init__(
        self,
        vector_retriever,
        bm25_retriever,
        top_k: int = settings.TOP_K,
        rrf_k: int = settings.RRF_K
    ):
        self.vector_retriever = vector_retriever
        self.bm25_retriever = bm25_retriever
        self.top_k = top_k

        self.rrf = RRFFusion(
            rrf_k=rrf_k
        )

    def retrieve(self, query: str) -> list[Document]:

        # Vector retrieval
        vector_docs = self.vector_retriever.retrieve(query)

        # BM25 retrieval
        bm25_docs = self.bm25_retriever.retrieve(query)

        # RRF Fusion
        fused_docs = self.rrf.fuse(
            ranked_lists=[
                vector_docs,
                bm25_docs
            ],
            top_k=self.top_k
        )

        return fused_docs



