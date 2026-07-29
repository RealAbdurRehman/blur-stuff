from flask import Blueprint, jsonify
from app.services.detectors import models

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    return jsonify({"status": "ok"})


@health_bp.get("/health/ready")
def ready():
    status = {name: model is not None for name, model in models.items()}
    ready = all(status.values())

    return jsonify({"status": "ready" if ready else "not_ready", "models": status}), (
        200 if ready else 503
    )
