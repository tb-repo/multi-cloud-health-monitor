"""API endpoints for health check data."""

from flask import Blueprint, jsonify

from app.models import FailoverEvent, HealthCheck

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/checks")
def get_health_checks():
    """Return recent health check history as JSON (last 50)."""
    checks = (
        HealthCheck.query.order_by(HealthCheck.timestamp.desc()).limit(50).all()
    )
    return jsonify([check.to_dict() for check in checks])


@api_bp.route("/status")
def get_multi_cloud_status():
    """Return current health status of all cloud deployments."""
    status = {}
    for cloud in ["aws", "azure", "gcp"]:
        latest = (
            HealthCheck.query.filter_by(target_cloud=cloud)
            .order_by(HealthCheck.timestamp.desc())
            .first()
        )
        if latest:
            status[cloud] = latest.to_dict()
        else:
            status[cloud] = {
                "target_cloud": cloud,
                "status": "unknown",
                "response_time_ms": None,
            }
    return jsonify(status)


@api_bp.route("/failovers")
def get_failover_events():
    """Return failover event history."""
    events = (
        FailoverEvent.query.order_by(FailoverEvent.timestamp.desc()).limit(20).all()
    )
    return jsonify([event.to_dict() for event in events])
