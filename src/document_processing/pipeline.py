# (1) Loader         ---- Done... 
# (2) Cleaner        ---- Done...
# (3) Splitter        ---- Done...
# (4) Embeddings ----  Done...
# (5) Vector store----  Done...

from src.document_processing.loader import load_data , PDFLoader
from src.document_processing.cleaner import CleanDocuments
from src.document_processing.vector_store import VectorStore
from src.document_processing.splitter import splite_document, RecursiveSplitter

def process_document_pipeline(path : str, embedding_model) :
    documnets = load_data( PDFLoader( path ) )
    documnets = CleanDocuments().clean_documents(documnets)

    chunks = splite_document( RecursiveSplitter(documents=documnets) )

    ids = VectorStore(embedding_model=embedding_model).add_chunks(chunks)

    return 'load - clean - split - save in vectorStore'