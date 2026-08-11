import gc
import os
from fastapi import APIRouter, UploadFile, Request
from src.helper.file_helper import save_temp_file
from src.document_processing import process_document_pipeline

process_document_router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

@process_document_router.post("/upload_file")
def upload_document(file: UploadFile, request : Request):
    temp_path = None
    # add validaton on file here
    try:
        temp_path = save_temp_file(file)
        message = process_document_pipeline(temp_path,
                                             embedding_model=request.app.state.embedding_model)

        return {
            "message": message
        }

    finally:
        file.file.close()
        gc.collect()

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)