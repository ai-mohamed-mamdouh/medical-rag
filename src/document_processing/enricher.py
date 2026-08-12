from langchain_core.documents import Document

class DocumentEnricher:
    """
    Enriches LangChain Documents by adding contextual metadata
    such as section and page information to page_content.
    """

    @staticmethod
    def enrich_documents(documents: list[Document]) -> list[Document]:
        result = []

        for document in documents:
            section = document.metadata.get("section", "Unknown")
            # page = document.metadata.get("page", "Unknown")

            context = (
                f"Section: {section}\n"
            )

            result.append(
                Document(
                    page_content=f"{context}\n{document.page_content}",
                    metadata=document.metadata.copy(),
                )
            )

        return result