from .root import root_bp
from .health import health_bp
from .detections import detections_bp
from .images import images_bp
from .videos import videos_bp

blueprints = [root_bp, health_bp, detections_bp, images_bp, videos_bp]
