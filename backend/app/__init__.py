from flask import Flask
from app.config import Config
from app.routes import register_routes
from pymongo import MongoClient
from langchain_cohere import CohereEmbeddings


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo_client = MongoClient(app.config['MONGODB_URI'])

    embedding_model = CohereEmbeddings(
        cohere_api_key=app.config['COHERE_API_KEY'],
        model="embed-english-v3.0"
    )

    app.mongo_client = mongo_client
    app.embedding_model = embedding_model

    register_routes(app)
    return app
