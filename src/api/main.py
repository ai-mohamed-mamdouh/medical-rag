from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.api.routes.document_processing import process_document_router
from src.document_processing.embeddings import get_embedding_model

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once when server starts
    app.state.embedding_model = get_embedding_model()

    yield

app = FastAPI(
    title="Medical RAG API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router( process_document_router )

@app.get("/")
def root():
    return {"message": "Medical RAG API is running"}