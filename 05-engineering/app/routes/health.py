"""Health check endpoint — used by load balancers and Route53."""

import time

from flask import Blueprint, current_app, jsonify

from app.models import db

health_bp = Blueprint("health", __name__)

# Track application start time for uptime calculation
_start_time = time.time()


@health_bp.route("/health")
def health_check():
    """
    Health endpoint for load balancer and DNS health checks.

    Returns 200 if healthy, 503 if database is unreachable.
    No authentication required.
    """
    # Check database connectivity
    db_connected = False
    try:
        db.session.execute(db.text("SELECT 1"))
        db_connected = True
    except Exception:
        pass

    uptime_seconds = int(time.time() - _start_time)
    status = "healthy" if db_connected else "unhealthy"
    status_code = 200 if db_connected else 503

    response = {
        "status": status,
        "db_connected": db_connected,
        "uptime_seconds": uptime_seconds,
        "cloud_provider": current_app.config["CLOUD_PROVIDER"],
        "region": current_app.config["CLOUD_REGION"],
        "instance_id": current_app.config["INSTANCE_ID"],
        "version": current_app.config["APP_VERSION"],
    }

    return jsonify(response), status_code
