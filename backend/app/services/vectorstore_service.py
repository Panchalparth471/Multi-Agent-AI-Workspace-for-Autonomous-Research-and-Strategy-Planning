from langchain.vectorstores import FAISS
from langchain.schema import Document
from app.utils.persistent_faiss import save_faiss_index, load_faiss_index

def index_documents(docs, embedding_model):
    vectorstore = FAISS.from_documents(docs, embedding_model)
    save_faiss_index(vectorstore)
    return vectorstore

def query_vectorstore(query, embedding_model, k=3):
    return search_documents(query, embedding_model, k)

def search_documents(query, embedding_model, k=3):
    vectorstore = load_faiss_index()
    if not vectorstore:
        return []
    return vectorstore.similarity_search(query, k=k)

def add_documents_to_index(docs, embedding_model):
    vectorstore = load_faiss_index()
    if vectorstore:
        vectorstore.add_documents(docs)
    else:
        vectorstore = FAISS.from_documents(docs, embedding_model)
    save_faiss_index(vectorstore)
