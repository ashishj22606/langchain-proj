from loader_registry import LOADER_REGISTRY, register_loader
from langchain.document_loaders import DirectoryLoader, TextLoader, UnstructuredPDFLoader, WebBaseLoader, CSVLoader, JSONLoader
from typing import List, Any
from langchain.schema import Document

@register_loader('text')
def load_text_documents(directory_path: str, **kwargs) -> List[Document]:
    loader = DirectoryLoader(
        directory_path,
        glob=kwargs.get('glob', '*.txt'),
        loader_cls=TextLoader,
        loader_kwargs={"autodetect_encoding": True},
        show_progress=True
    )
    return loader.load()

@register_loader('pdf')
def load_pdf_documents(directory_path: str, **kwargs) -> List[Document]:
    loader = DirectoryLoader(
        directory_path,
        glob=kwargs.get('glob', '*.pdf'),
        loader_cls=UnstructuredPDFLoader,
        show_progress=True
    )
    return loader.load()

@register_loader('web')
def load_web_documents(urls: List[str], **kwargs) -> List[Document]:
    loader = WebBaseLoader(urls)
    return loader.load()

@register_loader('csv')
def load_csv_documents(file_path: str, **kwargs) -> List[Document]:
    loader = CSVLoader(file_path)
    return loader.load()

@register_loader('json')
def load_json_documents(file_path: str, **kwargs) -> List[Document]:
    loader = JSONLoader(file_path)
    return loader.load()

def load_documents(source_type: str, source: Any, **kwargs) -> List[Document]:
    """
    Loads documents from various sources using the registered loader functions.
    Args:
        source_type (str): Type of the source ('text', 'pdf', 'web', 'csv', 'json', etc.)
        source (Any): Path, URL list, or other identifier for the data source.
        **kwargs: Additional arguments for the loader.
    Returns:
        List[Document]: List of loaded Document objects.
    """
    if source_type not in LOADER_REGISTRY:
        raise ValueError(f"No loader registered for source type: {source_type}")
    return LOADER_REGISTRY[source_type](source, **kwargs)

# Example: To add a new loader, use the @register_loader decorator
# @register_loader('my_new_source')
# def load_my_new_source(...):
#     ...
#     return docs
