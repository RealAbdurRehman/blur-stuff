from flask import Flask
from .routes import blueprints


def create_app():
    app = Flask(__name__)

    for bp in blueprints:
        app.register_blueprint(bp)

    return app
