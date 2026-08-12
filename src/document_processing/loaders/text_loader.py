from pathlib import Path
from datetime import datetime
from langchain_core.documents import Document

from src.document_processing.loaders import BaseLoader

class TextLoader(BaseLoader):
    """Load a text file with filesystem metadata."""

    def __init__(self, path: str):
        self.path = path

    def load(self) -> list[Document]:
        path = Path(self.path)

        # Read text content.
        text = path.read_text(encoding="utf-8")

        # File system metadata.
        stat = path.stat()

        metadata = {
            "source": str(path),
            "source_type": "text",
            "file_name": path.name,
            "file_stem": path.stem,
            "file_extension": path.suffix,
            "file_size_bytes": stat.st_size,
            "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        }

        return [
            Document(
                page_content=text,
                metadata=metadata,
            )
        ]