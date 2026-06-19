"""Database models for the Health Monitor application."""

from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class HealthCheck(db.Model):
    """Records health check results for all cloud endpoints."""

    __tablename__ = "health_checks"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    cloud_provider = db.Column(db.String(10), nullable=False)
    target_cloud = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(10), nullable=False)  # healthy, unhealthy, timeout
    response_time_ms = db.Column(db.Integer, nullable=True)
    details = db.Column(db.JSON, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "cloud_provider": self.cloud_provider,
            "target_cloud": self.target_cloud,
            "status": self.status,
            "response_time_ms": self.response_time_ms,
            "details": self.details,
        }


class DeploymentInfo(db.Model):
    """Records deployment identity for this instance."""

    __tablename__ = "deployment_info"

    id = db.Column(db.Integer, primary_key=True)
    cloud_provider = db.Column(db.String(10), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    instance_id = db.Column(db.String(100), nullable=True)
    deployed_at = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    version = db.Column(db.String(20), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "cloud_provider": self.cloud_provider,
            "region": self.region,
            "instance_id": self.instance_id,
            "deployed_at": self.deployed_at.isoformat() if self.deployed_at else None,
            "version": self.version,
        }


class FailoverEvent(db.Model):
    """Records failover events between clouds."""

    __tablename__ = "failover_events"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    from_cloud = db.Column(db.String(10), nullable=False)
    to_cloud = db.Column(db.String(10), nullable=False)
    reason = db.Column(db.Text, nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "from_cloud": self.from_cloud,
            "to_cloud": self.to_cloud,
            "reason": self.reason,
            "duration_seconds": self.duration_seconds,
        }
