# (1) Loader         ---- Done... 
# (2) Cleaner        ---- Done...
# (3) Splitter        ---- Done...
# (4) Embeddings ----
# (5) Vector store---- 

from src.document_processing.loader import load_data , PDFLoader
from src.document_processing.cleaner import CleanDocuments
from src.document_processing.splitter import splite_document, RecursiveSplitter

def file_process(path : str) :
    documnets = load_data( PDFLoader( path ) )
    documnets = CleanDocuments().clean_documents(documnets)

    chunks = splite_document( RecursiveSplitter(documents=documnets) )

    return chunks


if __name__ == '__main__' : 
    chunks = file_process( 'docs/Mohamed_Mamdouh.pdf' )
    print(chunks[0])