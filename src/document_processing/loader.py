from abc import ABC, abstractmethod
from langchain_core.documents import Document
from langchain_community.document_loaders import (TextLoader)
from langchain_pymupdf4llm import PyMuPDF4LLMLoader

class BaseLoader (ABC):
    @abstractmethod
    def load(self) ->list[Document]: 
        raise NotImplementedError


class PDFLoader(BaseLoader) :
    def __init__(self, path) :
        self.path = path

    def load(self)->list[Document] :
        return PyMuPDF4LLMLoader(self.path, mode="page").load()

    
class TXTLoader(BaseLoader) :
    def __init__(self, path) :
        self.path = path

    def load(self)->list[Document] :
        return TextLoader(self.path).load()


def load_data(loader: BaseLoader) -> list[Document] :
    """args : loader -> loaderName(file_path)"""
    documents = loader.load()
    return documents


# # For try .......
# if __name__ == '__main__' : 
#     documents = load_data( TXTLoader('docs/test.txt') )
#     print("========================================")
#     print(type(documents))
#     print("========================================")
#     print(len(documents))
#     print("========================================")
#     print(documents[0].page_content)
#     print("========================================")