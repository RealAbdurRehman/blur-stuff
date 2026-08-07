from flask import render_template
from app.frontend import frontend_bp


@frontend_bp.get("/anonymize")
def anonymize():
    return render_template("anonymize.html")
