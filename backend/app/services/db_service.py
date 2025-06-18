from flask import current_app
import datetime
def get_mongo_collection(collection_name):
    db = current_app.mongo_client.get_default_database()
    return db[collection_name]

def save_document(collection_name, document):
    collection = get_mongo_collection(collection_name)
    return collection.insert_one(document).inserted_id

def fetch_documents(collection_name, query={}, limit=10):
    collection = get_mongo_collection(collection_name)
    return list(collection.find(query).limit(limit))

def save_feedback_step(stage, rating, feedback, suggestion):
    doc = {
        "stage": stage,
        "rating": rating,
        "feedback": feedback,
        "suggestion": suggestion,
        "timestamp": datetime.utcnow()
    }
    save_document("agent_feedback", doc)