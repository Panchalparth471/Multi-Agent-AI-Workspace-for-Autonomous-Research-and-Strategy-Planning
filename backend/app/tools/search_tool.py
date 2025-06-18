import os
from langchain.tools import Tool
from functools import partial
from app.services.vectorstore_service import search_documents
from app.services.embedding_service import get_embedding_model
from langchain_community.utilities.serpapi import SerpAPIWrapper
from app.services.vectorstore_service import query_vectorstore

def get_web_search_tool():
    search = SerpAPIWrapper(serpapi_api_key=os.getenv("SERPAPI_API_KEY"))
    return Tool(
        name="Web Search",
        func=search.run,
        description="Search the web using SerpAPI for up-to-date information."
    )
    
def local_vector_search(query: str) -> str:
    try:
        embedding_model = get_embedding_model()
        results = search_documents(query, embedding_model, k=3)
        return "\n".join([doc.page_content for doc in results])
    except Exception as e:
        return f"Vector search failed: {str(e)}"

def get_local_vector_search_tool():
    return Tool(
        name="Local Vector Search",
        func=local_vector_search,
        description="Searches local FAISS vector store for relevant documents."
    )



def get_search_tools():
    return [
        get_web_search_tool(),
        get_local_vector_search_tool()
    ]
