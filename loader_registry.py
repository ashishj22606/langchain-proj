from typing import List, Callable, Dict
from langchain.schema import Document

# Registry for loader functions by source type
LOADER_REGISTRY: Dict[str, Callable[..., List[Document]]] = {}

def register_loader(source_type: str):
    """Decorator to register a new loader function."""
    def decorator(func):
        LOADER_REGISTRY[source_type] = func
        return func
    return decorator
