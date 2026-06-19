"""WSGI entry point for Gunicorn.

This module is the entry point referenced by the Gunicorn command.
File location: /opt/healthmonitor/wsgi.py inside Docker container.
Python path includes /opt/healthmonitor so 'app' package is importable.
"""

from app.app import create_app

application = create_app()

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000)
