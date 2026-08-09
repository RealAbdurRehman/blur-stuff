from flask import render_template
from app.frontend import frontend_bp


@frontend_bp.get("/detect")
def detect():
    return render_template("detect.html")


@frontend_bp.get("/results")
def results():
    return render_template("results.html")
