"""Application configuration loaded from environment variables."""

import os


class Config:
    """Base configuration."""

    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"

    # Database
    DATABASE_URL = os.environ.get(
        "DATABASE_URL", "postgresql://healthmon:healthmon@db:5432/healthmonitor"
    )
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cloud Identity
    CLOUD_PROVIDER = os.environ.get("CLOUD_PROVIDER", "local")
    CLOUD_REGION = os.environ.get("CLOUD_REGION", "local")
    DEPLOYMENT_ID = os.environ.get("DEPLOYMENT_ID", "local-dev")
    INSTANCE_ID = os.environ.get("INSTANCE_ID", "local")

    # Health Check Targets (other cloud endpoints)
    HEALTH_CHECK_TARGETS = {
        "aws": os.environ.get("HEALTH_TARGET_AWS", ""),
        "azure": os.environ.get("HEALTH_TARGET_AZURE", ""),
        "gcp": os.environ.get("HEALTH_TARGET_GCP", ""),
    }

    # Health Check Interval (seconds)
    HEALTH_CHECK_INTERVAL = int(os.environ.get("HEALTH_CHECK_INTERVAL", "30"))

    # Application Info
    APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")
