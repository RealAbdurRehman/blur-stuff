from flask import render_template
from app.frontend import frontend_bp
from app.ui_data import FEATURES


@frontend_bp.get("/")
def index():
    return render_template("index.html", features=FEATURES)
