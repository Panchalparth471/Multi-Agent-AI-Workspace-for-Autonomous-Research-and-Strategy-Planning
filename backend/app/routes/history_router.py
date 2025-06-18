# routes/history_router.py
from flask import Blueprint, jsonify
from app.services.db_service import fetch_documents

history_bp = Blueprint("history", __name__, url_prefix="/pipeline-history")

@history_bp.route("/", methods=["GET"])
def get_past_runs():
    docs = fetch_documents("pipeline_results", limit=5)
    return jsonify(docs)
