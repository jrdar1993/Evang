from flask import Blueprint

health_bp = Blueprint('health', __name__)

@health_bp.route("/health", methods=["GET"])
def health():
    return "OK", 200
