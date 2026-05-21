# NumberCal — production Dockerfile
# Build:  docker build -t numbercal .
# Run:    docker run -p 8000:8000 numbercal
#
# For VPS deployment:
#   1. Copy this repo to your server
#   2. Install Docker
#   3. docker build -t numbercal .
#   4. docker run -d --name numbercal --restart=always -p 127.0.0.1:8000:8000 numbercal
#   5. Configure nginx as reverse proxy (see PRODUCTION_READINESS.md)

FROM python:3.12-slim

# Don't write .pyc, unbuffered stdout for proper logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash numbercals

WORKDIR /app

# Install deps first (cached layer)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copy app
COPY backend/ .
RUN chown -R numbercals:numbercals /app

USER numbercals

# Healthcheck for the orchestrator
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/healthz').read()" || exit 1

EXPOSE 8000

# 4 workers is a reasonable default for a 2-vCPU VPS; adjust based on your VPS size.
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "-b", "0.0.0.0:8000", "main:app"]
