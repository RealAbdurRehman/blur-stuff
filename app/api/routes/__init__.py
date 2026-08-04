from flask import Blueprint

from .root import root_bp
from .health import health_bp
from .detections import detections_bp
from .images import images_bp
from .videos import videos_bp
from .documents import documents_bp

api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")

api_v1.register_blueprint(health_bp)
api_v1.register_blueprint(detections_bp)
api_v1.register_blueprint(images_bp)
api_v1.register_blueprint(videos_bp)
api_v1.register_blueprint(documents_bp)

blueprints = [root_bp, api_v1]
