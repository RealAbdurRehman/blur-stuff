from flask import render_template
from app.frontend import frontend_bp


@frontend_bp.get("/privacy")
def privacy():
    return render_template("privacy.html")
