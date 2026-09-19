from functools import lru_cache
from pathlib import Path

from langchain_core.documents import Document
from langchain_core.tools import tool
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

RUNBOOK_PATH = (
     Path(__file__).resolve().parents[2]
    / "runbooks"
    / "data_ingestion.md"
)


@lru_cache(maxsize=1)
def build_vector_store():
    runbook_text = RUNBOOK_PATH.read_text()
    chunks = [chunk.strip() for chunk in runbook_text.split("\n\n") if chunk.strip()]
    documents = [Document(page_content=chunk,metadata={"source": str(RUNBOOK_PATH)}) for chunk in chunks]

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vector_store = InMemoryVectorStore(
        embedding=embeddings
    )

    vector_store.add_documents(documents)

    return vector_store

@tool
def search_runbook_semantically(query:str) -> list[dict]:
    """Search the operational runbook for passages relevant to a question."""
    vector_store = build_vector_store()
    results = vector_store.similarity_search(
        query,
        k=2
    )
    return [
        {
            "content": document.page_content,
            "source": document.metadata["source"]
        }
        for document in results
    ]

