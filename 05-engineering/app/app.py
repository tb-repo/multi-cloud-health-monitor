"""Flask application factory."""

import logging
import sys

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

from app.config import Config
from app.models import DeploymentInfo, db
from app.routes.api import api_bp
from app.routes.dashboard import dashboard_bp
from app.routes.health import health_bp
from app.services.health_checker import run_health_checks


def configure_logging():
    """Configure structured JSON-like logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def create_app(config_class=Config):
    """Create and configure the Flask application."""
    configure_logging()
    logger = logging.getLogger(__name__)

    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config_class)

    # Initialize database
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(api_bp)

    # Initialize Prometheus metrics (exposes /metrics endpoint automatically)
    PrometheusMetrics(app)

    # Create tables and register deployment
    with app.app_context():
        db.create_all()
        _register_deployment(app, logger)

    # Start background health checker
    _start_health_checker(app, logger)

    logger.info(
        "Application started: cloud=%s region=%s instance=%s",
        app.config["CLOUD_PROVIDER"],
        app.config["CLOUD_REGION"],
        app.config["INSTANCE_ID"],
    )

    return app


def _register_deployment(app, logger):
    """Record this deployment in the database."""
    try:
        deployment = DeploymentInfo(
            cloud_provider=app.config["CLOUD_PROVIDER"],
            region=app.config["CLOUD_REGION"],
            instance_id=app.config["INSTANCE_ID"],
            version=app.config["APP_VERSION"],
        )
        db.session.add(deployment)
        db.session.commit()
        logger.info("Deployment registered in database")
    except Exception as e:
        logger.warning("Failed to register deployment: %s", str(e))
        db.session.rollback()


def _start_health_checker(app, logger):
    """Start the background health check scheduler."""
    interval = app.config["HEALTH_CHECK_INTERVAL"]

    # Only start if there are configured targets
    targets = app.config["HEALTH_CHECK_TARGETS"]
    has_targets = any(url for url in targets.values() if url)

    if not has_targets:
        logger.info("No health check targets configured. Scheduler not started.")
        return

    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(
        func=run_health_checks,
        trigger="interval",
        seconds=interval,
        args=[app],
        id="health_checker",
        name="Multi-Cloud Health Checker",
    )
    scheduler.start()
    logger.info("Health checker started with %ds interval", interval)
