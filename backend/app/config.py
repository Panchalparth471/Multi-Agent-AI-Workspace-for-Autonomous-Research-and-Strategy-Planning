import os
from dotenv import load_dotenv
from pymongo import MongoClient, errors

load_dotenv()

class Config:
   
    MONGODB_URI = os.getenv("MONGODB_URI")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    COHERE_API_KEY = os.getenv("COHERE_API_KEY") 
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")


    LANGCHAIN_TRACING_V2 = True
    LANGCHAIN_PROJECT = "AgentSystem"

    
    try:
        mongo_client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        mongo_client.admin.command("ping") 
        print(" MongoDB connected successfully")
        mongo_db = mongo_client["LLM"]
    except errors.ServerSelectionTimeoutError as e:
        print(f" MongoDB connection failed: {e}")
        mongo_client = None
        mongo_db = None
