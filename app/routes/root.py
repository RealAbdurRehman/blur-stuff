from flask import Blueprint, jsonify

root_bp = Blueprint("root", __name__)


@root_bp.get("/")
def index():
    return jsonify({"name": "Blur Stuff"})
