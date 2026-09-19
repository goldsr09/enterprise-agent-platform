from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    model = "text-embedding-3-small"
)

vector = embeddings.embed_query(
    "Android traffic suddenly decreased"
)

print("vector length:",len(vector))
print("first five values:",vector[:5])

