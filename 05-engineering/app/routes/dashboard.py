"""Dashboard route — main UI page."""

from flask import Blueprint, current_app, render_template

from app.models import DeploymentInfo, FailoverEvent, HealthCheck, db

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def index():
    """Render the main health monitor dashboard."""
    # Get latest health checks per target cloud
    cloud_status = {}
    for cloud in ["aws", "azure", "gcp"]:
        latest_check = (
            HealthCheck.query.filter_by(target_cloud=cloud)
            .order_by(HealthCheck.timestamp.desc())
            .first()
        )
        if latest_check:
            cloud_status[cloud] = latest_check.to_dict()
        else:
            cloud_status[cloud] = {"status": "unknown", "target_cloud": cloud}

    # Get recent health check history (last 50)
    recent_checks = (
        HealthCheck.query.order_by(HealthCheck.timestamp.desc()).limit(50).all()
    )

    # Get last failover event
    last_failover = (
        FailoverEvent.query.order_by(FailoverEvent.timestamp.desc()).first()
    )

    # Current deployment info
    deployment = {
        "cloud_provider": current_app.config["CLOUD_PROVIDER"],
        "region": current_app.config["CLOUD_REGION"],
        "instance_id": current_app.config["INSTANCE_ID"],
        "version": current_app.config["APP_VERSION"],
    }

    return render_template(
        "dashboard.html",
        cloud_status=cloud_status,
        recent_checks=recent_checks,
        last_failover=last_failover,
        deployment=deployment,
    )
