# (1) Loader         ---- Done... 
# (2) Cleaner        ---- Done...
# (3) Splitter        ---- Done...
# (4) Embeddings ----  Done...
# (5) Vector store----  Done...

from src.document_processing.loader import load_data , PDFLoader
from src.document_processing.cleaner import CleanDocuments
from src.document_processing.splitter import splite_document, RecursiveSplitter
from src.document_processing.vector_store import VectorStore

def file_process(path : str) :
    documnets = load_data( PDFLoader( path ) )
    documnets = CleanDocuments().clean_documents(documnets)

    chunks = splite_document( RecursiveSplitter(documents=documnets) )

    ids = VectorStore().add_chunks(chunks)

    return ids