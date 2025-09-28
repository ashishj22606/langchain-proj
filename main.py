from document_loader import load_documents
import yaml
import os
from typing import Any
import json
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def apply_embedding(docs, model_name):
    model = SentenceTransformer(model_name)
    texts = [doc.page_content for doc in docs]
    embeddings = model.encode(texts)
    for doc, emb in zip(docs, embeddings):
        doc.metadata['embedding'] = emb.tolist()
    return docs

def sanitize_metadata(metadata):
    # Only allow str, int, float, bool, None
    return {k: (str(v) if not isinstance(v, (str, int, float, bool, type(None))) else v) for k, v in metadata.items()}

def store_documents(docs, target: dict):
    target_type = target.get('type')
    if target_type == 'file':
        path = target.get('path')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        # Store as JSON lines
        with open(path, 'w', encoding='utf-8') as f:
            for doc in docs:
                json.dump({'content': doc.page_content, 'metadata': doc.metadata}, f)
                f.write('\n')
    elif target_type == 'vectordb':
        db_type = target.get('db_type', 'chroma')
        if db_type == 'chroma':
            persist_path = target.get('path', 'output/chroma_db')
            client = chromadb.PersistentClient(path=persist_path)
            collection = client.get_or_create_collection(name="rag_collection")
            for i, doc in enumerate(docs):
                safe_metadata = sanitize_metadata(doc.metadata)
                collection.add(
                    embeddings=[doc.metadata['embedding']],
                    documents=[doc.page_content],
                    ids=[str(i)],
                    metadatas=[safe_metadata]
                )
            print(f"[INFO] Stored {len(docs)} docs in ChromaDB at {persist_path}")
        else:
            print(f"[WARN] Unknown vector DB type: {db_type}")
    else:
        print(f"[WARN] Unknown target type: {target_type}")

def chunk_documents(docs, chunk_size=512, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunked_docs = []
    for doc in docs:
        chunks = splitter.split_text(doc.page_content)
        for i, chunk in enumerate(chunks):
            # Create a new doc for each chunk, preserve metadata
            new_doc = type(doc)(page_content=chunk, metadata={**doc.metadata, "chunk_id": i})
            chunked_docs.append(new_doc)
    return chunked_docs

def process_sources_from_yaml(yaml_path: str):
    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)
    for src in config.get('sources', []):
        print(f"[INFO] Processing source: {src['name']}")
        docs = load_documents(src['type'], src['source'], **src.get('params', {}))
        print(f"[DEBUG] Loaded {len(docs)} docs for source: {src['name']}")
        if 'embedding_model' in src:
            print(f"[DEBUG] Applying embedding model: {src['embedding_model']}")
            chunk_size = src.get('chunk_size', 512)
            chunk_overlap = src.get('chunk_overlap', 50)
            docs = chunk_documents(docs, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            docs = apply_embedding(docs, src['embedding_model'])
            print(f"[DEBUG] Example embedding: {docs[0].metadata.get('embedding') if docs else 'No docs'}")
        if 'target' in src:
            print(f"[DEBUG] Storing {len(docs)} docs to target: {src['target']}")
            store_documents(docs, src['target'])
        print(f"[INFO] Finished source: {src['name']}\n")

def main():
    # Example usage: load documents from a directory
    docs = load_documents('sample_docs')
    for doc in docs:
        print(f"Loaded document: {doc.metadata.get('source', 'unknown')}")
        print(doc.page_content[:200])  # Print first 200 chars
        print('-' * 40)
    process_sources_from_yaml('sources.yml')

if __name__ == "__main__":
    process_sources_from_yaml('sources.yml')
