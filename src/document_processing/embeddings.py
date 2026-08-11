# return embedding model only ... any provider , any model
from src.config.settings import settings
from langchain_huggingface import HuggingFaceEmbeddings

def get_embedding_model() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL_NAME
    )
