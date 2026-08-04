from flask import render_template
from app.frontend import frontend_bp


@frontend_bp.get("/")
def index():
    return render_template("index.html")
