from src.document_processing.loaders import BaseLoader, PDFLoader
from src.document_processing.cleaner import CleanDocuments
from langchain_core.documents import Document

def load_data(loader: BaseLoader) -> list[Document]:
    """
    Load documents using the provided loader.

    Args:
        loader: An initialized BaseLoader implementation.

    Returns:
        A list of LangChain Document objects.
    """
    return loader.load()

if __name__ == '__main__' :
    documents = load_data( PDFLoader('docs/giddiness.pdf'))
    documents = CleanDocuments().clean_documents(documents=documents)
    documents = CleanDocuments().split_preserving_tables(documents[3].page_content)

    print('=================') 
    print(type(documents))
    print('=================') 
    print(len(documents))
    print('=================') 
    print(documents[0].page_content)
