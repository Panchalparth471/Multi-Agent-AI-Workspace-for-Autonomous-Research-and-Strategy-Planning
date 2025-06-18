from flask import Blueprint



from .agent_pipeline import agent_pipeline_bp
from .history_router import history_bp

def register_routes(app):
    app.register_blueprint(agent_pipeline_bp)
    app.register_blueprint(history_bp)