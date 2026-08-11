from langchain_chroma import Chroma
from langchain_core.documents import Document
from src.document_processing.embeddings import get_embedding_model

class VectorStore:
    def __init__(self):
        self.embedding_model = get_embedding_model()
        self.vector_store = self.get_vector_store()

    def get_vector_store(self) -> Chroma:
        return Chroma(
            collection_name="medical_collection",
            embedding_function=self.embedding_model,
            persist_directory="./chroma_db",
        )

    def add_chunks(self, chunks: list[Document]) -> list[str]:
        return self.vector_store.add_documents(chunks)