from src.document_processing.loaders import (
    BaseLoader,
    PDFLoader,
    TextLoader,
    URLLoader
)
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


# For try .......
if __name__ == '__main__' : 
    documents = load_data( PDFLoader('docs/giddiness.pdf') )
    print("========================================")
    print(type(documents))
    print("========================================")
    print(len(documents))
    print("========================================")
    print(documents[0].page_content)
    print("========================================")