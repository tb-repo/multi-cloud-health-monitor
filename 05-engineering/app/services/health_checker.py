"""Background health checker service.

Periodically checks the health of all configured cloud endpoints
and records results in the database.
"""

import logging
import time

import requests

from app.models import HealthCheck, db

logger = logging.getLogger(__name__)


def check_endpoint(target_cloud: str, url: str, cloud_provider: str) -> HealthCheck:
    """
    Check a single cloud endpoint and return a HealthCheck record.

    Args:
        target_cloud: Which cloud we are checking (aws, azure, gcp)
        url: The health endpoint URL to check
        cloud_provider: Which cloud THIS instance is running on

    Returns:
        HealthCheck model instance (not yet committed to DB)
    """
    if not url:
        return HealthCheck(
            cloud_provider=cloud_provider,
            target_cloud=target_cloud,
            status="unconfigured",
            response_time_ms=None,
            details={"error": "No endpoint configured"},
        )

    try:
        start = time.time()
        response = requests.get(f"{url}/health", timeout=10)
        elapsed_ms = int((time.time() - start) * 1000)

        if response.status_code == 200:
            status = "healthy"
            details = response.json()
        else:
            status = "unhealthy"
            details = {"status_code": response.status_code}

    except requests.Timeout:
        elapsed_ms = 10000
        status = "timeout"
        details = {"error": "Request timed out (10s)"}

    except requests.ConnectionError as e:
        elapsed_ms = None
        status = "unhealthy"
        details = {"error": f"Connection failed: {str(e)[:200]}"}

    except Exception as e:
        elapsed_ms = None
        status = "unhealthy"
        details = {"error": f"Unexpected error: {str(e)[:200]}"}

    return HealthCheck(
        cloud_provider=cloud_provider,
        target_cloud=target_cloud,
        status=status,
        response_time_ms=elapsed_ms,
        details=details,
    )


def run_health_checks(app):
    """
    Run health checks against all configured cloud targets.

    This function is called by the APScheduler background job.
    """
    with app.app_context():
        cloud_provider = app.config["CLOUD_PROVIDER"]
        targets = app.config["HEALTH_CHECK_TARGETS"]

        for target_cloud, url in targets.items():
            if not url:
                continue

            check = check_endpoint(target_cloud, url, cloud_provider)
            db.session.add(check)

            logger.info(
                "Health check: %s -> %s = %s (%s ms)",
                cloud_provider,
                target_cloud,
                check.status,
                check.response_time_ms,
            )

        try:
            db.session.commit()
        except Exception as e:
            logger.error("Failed to save health checks: %s", str(e))
            db.session.rollback()
