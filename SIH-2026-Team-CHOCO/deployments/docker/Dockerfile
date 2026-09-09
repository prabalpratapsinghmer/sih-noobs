# syntax=docker/dockerfile:1
# ============================================================================
# SIH26184 — Cybercrime Prediction API (CPU Image)
# ============================================================================
FROM python:3.11-slim AS base

LABEL maintainer="SIH Team <team@sih.gov.in>"
LABEL description="Predictive Analytics Framework for Cybercrime Complaints"

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN groupadd -r sih && useradd -r -g sih -d /app -s /sbin/nologin sih \
    && chown -R sih:sih /app
USER sih

# Create necessary directories
RUN mkdir -p logs mlflow/experiments mlflow/models data/raw data/processed

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose API port
EXPOSE 8000

# Default command: start the API server
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
