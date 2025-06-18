# routes/agent_pipeline.py
from flask import Blueprint, request, jsonify
from app.agents.pipeline_agent import run_full_pipeline

agent_pipeline_bp = Blueprint("agent_pipeline", __name__, url_prefix="/agent-pipeline")

@agent_pipeline_bp.route("/run", methods=["POST"])
def run_pipeline():
    data = request.json
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "Missing 'query'"}), 400

    output = run_full_pipeline(query)
    return jsonify(output)
