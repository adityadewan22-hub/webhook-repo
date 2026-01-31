from flask import Blueprint, send_from_directory

ui_bp = Blueprint("ui", __name__)

@ui_bp.route("/ui")
def serve_ui():
    return send_from_directory("ui", "index.html")

@ui_bp.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory("ui", path)
