"""Gunicorn configuration file."""

import os

# Server socket
bind = "0.0.0.0:5000"

# Worker processes
workers = int(os.environ.get("GUNICORN_WORKERS", "2"))
worker_class = "sync"
timeout = 120

# Logging
accesslog = "-"
errorlog = "-"
loglevel = os.environ.get("LOG_LEVEL", "info")

# Process naming
proc_name = "health-monitor"

# Preload application for better memory usage
preload_app = True
