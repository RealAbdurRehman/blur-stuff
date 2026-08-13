from flask import render_template
from app.frontend import frontend_bp


@frontend_bp.get("/api")
def api():
    return render_template("api.html")
