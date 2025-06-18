from langchain.schema import Document
from typing import List

def summarize_documents(docs: List[Document]) -> str:
    return "\n".join([doc.page_content[:100] + "..." for doc in docs])


def flatten_dict(d: dict, parent_key: str = '', sep: str = '.') -> dict:
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
