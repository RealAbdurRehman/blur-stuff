from flask import render_template
from app.frontend import frontend_bp


@frontend_bp.get("/docs")
def docs():
    return render_template("docs.html")
