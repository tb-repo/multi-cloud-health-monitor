# Multi-Cloud Resource Health Monitor
# Multi-stage build for optimized production image

# Stage 1: Build dependencies
FROM python:3.13-slim AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Stage 2: Production
FROM python:3.13-slim

# Security: run as non-root user
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /opt/healthmonitor

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY . app/

# Set ownership
RUN chown -R appuser:appuser /opt/healthmonitor

USER appuser

# Environment defaults
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/opt/healthmonitor

EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import requests; r=requests.get('http://localhost:5000/health'); exit(0 if r.status_code==200 else 1)"

# Run with Gunicorn
CMD ["gunicorn", "--config", "app/gunicorn.conf.py", "app.wsgi:application"]
