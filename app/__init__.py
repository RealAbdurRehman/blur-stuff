from flask import Flask

from .frontend import frontend_bp
from .api.routes import blueprints as api_bps


def create_app():
    app = Flask(__name__, static_folder=None, template_folder=None)

    app.register_blueprint(frontend_bp)
    for bp in api_bps:
        app.register_blueprint(bp)

    return app
