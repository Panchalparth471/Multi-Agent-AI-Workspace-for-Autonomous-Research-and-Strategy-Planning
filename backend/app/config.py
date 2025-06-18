import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGODB_URI = os.getenv("MONGODB_URI")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    COHERE_API_KEY = os.getenv("COHERE_API_KEY") 
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
    LANGCHAIN_TRACING_V2 = True
    LANGCHAIN_PROJECT = "AgentSystem"
