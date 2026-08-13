from flask import render_template
from app.frontend import frontend_bp


@frontend_bp.get("/about")
def about():
    return render_template("about.html")
