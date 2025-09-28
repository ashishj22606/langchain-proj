import chromadb
from chromadb.config import Settings

persist_path = "output/sample_web_chroma"
client = chromadb.Client(Settings(persist_directory=persist_path))
print("Collections:", client.list_collections())
collection = client.get_collection("rag_collection")

# Fetch all document IDs
ids = collection.get()["ids"]

# Fetch documents and metadata for each ID
for id in ids:
    result = collection.get(ids=[id])
    print("ID:", id)
    print("Document:", result["documents"][0])
    print("Metadata:", result["metadatas"][0])
    print("-" * 40)