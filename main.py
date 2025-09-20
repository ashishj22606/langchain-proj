from document_loader import load_documents
import yaml
import os
from typing import Any
import json

def apply_embedding(docs, model_name):
    # Placeholder: Replace with actual embedding logic
    # For now, just add a dummy embedding field
    for doc in docs:
        doc.metadata['embedding'] = f"embedding_with_{model_name}"
    return docs

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
        # Placeholder: Add logic for vector DB storage
        print(f"[INFO] Would store {len(docs)} docs in vector DB at {target.get('path')}")
    else:
        print(f"[WARN] Unknown target type: {target_type}")

def process_sources_from_yaml(yaml_path: str):
    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)
    for src in config.get('sources', []):
        print(f"[INFO] Processing source: {src['name']}")
        docs = load_documents(src['type'], src['source'], **src.get('params', {}))
        if 'embedding_model' in src:
            docs = apply_embedding(docs, src['embedding_model'])
        if 'target' in src:
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
