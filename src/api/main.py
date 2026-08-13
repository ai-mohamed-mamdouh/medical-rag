from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI

from src.api.routes.document_processing import document_processing_router
from src.document_processing.embeddings import Embedding

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading embedding model...")

    app.state.embedding_model = Embedding().get_embedding_model()

    logger.info("Embedding model loaded successfully.")

    yield

    # Optional cleanup on application shutdown
    app.state.embedding_model = None

    logger.info("Application shutdown complete.")

app = FastAPI(
    title="Medical RAG API",
    description="API for document ingestion and medical RAG operations.",
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(document_processing_router)


@app.get("/", tags=["Health"])
def root():
    return {
        "status": "ok",
        "message": "Medical RAG API is running",
    }