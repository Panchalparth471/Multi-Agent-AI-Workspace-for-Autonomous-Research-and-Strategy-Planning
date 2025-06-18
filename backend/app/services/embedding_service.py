from langchain_cohere import CohereEmbeddings
import os

def get_embedding_model():
    return CohereEmbeddings(cohere_api_key=os.getenv("COHERE_API_KEY"), model="embed-english-v3.0" )
