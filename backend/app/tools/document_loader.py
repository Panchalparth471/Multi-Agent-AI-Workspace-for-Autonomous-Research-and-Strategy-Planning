from langchain.document_loaders import TextLoader
from langchain.schema import Document
from typing import List

def load_documents_from_texts(texts: List[str]) -> List[Document]:
    return [Document(page_content=text) for text in texts]

