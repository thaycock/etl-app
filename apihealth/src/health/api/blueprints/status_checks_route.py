from flask import Blueprint, jsonify

status_checks_bp = Blueprint("status_checks", __name__)


@status_checks_bp.route("/status", methods=["GET"])
def get_public_status_check() -> jsonify:
    return jsonify(
        {
            "success": True,
            "message": "Public status check endpoint is operational",
        }
    )
