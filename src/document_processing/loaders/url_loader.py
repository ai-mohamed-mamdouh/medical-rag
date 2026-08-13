import fitz
import pymupdf4llm
import requests
from bs4 import BeautifulSoup
from langchain_core.documents import Document

from src.document_processing.loaders import BaseLoader

class URLLoader(BaseLoader):
    """Load a webpage and extract useful HTML metadata."""

    def __init__(self, url: str):
        self.url = url

    def load(self) -> list[Document]:
        response = requests.get(
            self.url,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract common page metadata.
        title = soup.title.string.strip() if soup.title and soup.title.string else None

        description_tag = soup.find(
            "meta",
            attrs={"name": "description"},
        )

        author_tag = soup.find(
            "meta",
            attrs={"name": "author"},
        )

        language = (
            soup.html.get("lang")
            if soup.html
            else None
        )

        canonical_tag = soup.find(
            "link",
            attrs={"rel": "canonical"},
        )

        og_title = soup.find(
            "meta",
            attrs={"property": "og:title"},
        )

        og_description = soup.find(
            "meta",
            attrs={"property": "og:description"},
        )

        og_image = soup.find(
            "meta",
            attrs={"property": "og:image"},
        )

        published_time = soup.find(
            "meta",
            attrs={"property": "article:published_time"},
        )

        # Remove noisy HTML elements.
        for tag in soup(
            [
                "script",
                "style",
                "nav",
                "footer",
                "header",
                "noscript",
            ]
        ):
            tag.decompose()

        text = soup.get_text(
            separator="\n",
            strip=True,
        )

        metadata = {
            "source": self.url,
            "source_type": "url",

            # HTTP metadata
            "final_url": response.url,
            "status_code": response.status_code,
            "content_type": response.headers.get("Content-Type"),
            "content_length": response.headers.get("Content-Length"),
            "server": response.headers.get("Server"),
            "last_modified": response.headers.get("Last-Modified"),

            # HTML metadata
            "title": title,
            "description": (
                description_tag.get("content")
                if description_tag
                else None
            ),
            "author": (
                author_tag.get("content")
                if author_tag
                else None
            ),
            "language": language,
            "canonical_url": (
                canonical_tag.get("href")
                if canonical_tag
                else None
            ),

            # OpenGraph metadata
            "og_title": (
                og_title.get("content")
                if og_title
                else None
            ),
            "og_description": (
                og_description.get("content")
                if og_description
                else None
            ),
            "og_image": (
                og_image.get("content")
                if og_image
                else None
            ),

            "published_at": (
                published_time.get("content")
                if published_time
                else None
            ),
        }

        # Remove metadata fields with no value.
        metadata = {
            key: value
            for key, value in metadata.items()
            if value is not None
        }

        return [
            Document(
                page_content=text,
                metadata=metadata,
            )
        ]