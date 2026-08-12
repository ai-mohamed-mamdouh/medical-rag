from abc import ABC, abstractmethod
from src.config.settings import settings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

class BaseSplitter(ABC) :
    @abstractmethod
    def splite(self) :
        raise NotImplementedError

class FixedSplitter (BaseSplitter) : 
    def __init__(self,  documents) :
        self.documents = documents
    def splite (self) : 
        raise NotImplementedError

class SemanticSplitter (BaseSplitter) : 
    def __init__(self,  documents) :
        self.documents = documents
    def splite (self) : 
        raise NotImplementedError

    
class RecursiveSplitter (BaseSplitter) : 
    def __init__(self, documents) :
        self.documents = documents

    def splite(self) -> list[Document]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=['\n\n' ,'\n' , ' ' , '']
            )

        return splitter.split_documents(self.documents) # List of chunks 


def splite_document( splitter : BaseSplitter ) -> list[Document]:
    return splitter.splite() # List of chunks