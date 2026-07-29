from flask import Blueprint, request, jsonify

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return jsonify({"status": "ok"})


@main.route("/images", methods=["POST"])
def images():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "File must have a name"}), 400

    if not file.content_type.startswith("image/"):
        return jsonify({"error": "File must be an image"}), 400

    data = file.read()
    return jsonify(
        {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(data),
        }
    )
