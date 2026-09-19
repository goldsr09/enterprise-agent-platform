from pathlib import Path

from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings


runbook_path = Path("runbooks/data_ingestion.md")
runbook_text = runbook_path.read_text()
chunks = [chunk.strip() for chunk in runbook_text.split("\n\n") if chunk.strip()]

documents = [Document(page_content=chunk,metadata={"source": str(runbook_path)}) for chunk in chunks]

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vector_store = InMemoryVectorStore(
    embedding=embeddings
)

vector_store.add_documents(documents)

results = vector_store.similarity_search(
 "What should I investigate when Android traffic drops?",
 k=2
)

for number, document in enumerate(results, start=1):
    print(f"\nResult {number}")
    print("Source:", document.metadata["source"])
    print(document.page_content)