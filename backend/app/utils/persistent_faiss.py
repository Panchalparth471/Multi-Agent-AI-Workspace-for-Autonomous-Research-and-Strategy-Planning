import os
from langchain_community.vectorstores import FAISS
from flask import current_app

FAISS_INDEX_PATH = "app/storage/faiss_index"

def save_faiss_index(faiss_index):
    os.makedirs(FAISS_INDEX_PATH, exist_ok=True)
    faiss_index.save_local(FAISS_INDEX_PATH)

def load_faiss_index():
    embedding_model = current_app.embedding_model
    if not os.path.exists(FAISS_INDEX_PATH):
        return None
    return FAISS.load_local(FAISS_INDEX_PATH, embedding_model,allow_dangerous_deserialization=True)
