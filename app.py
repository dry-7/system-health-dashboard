
import json
import os
import time
from datetime import datetime, timezone

from flask import Flask, Response, g, jsonify, request
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)

app = Flask(__name__)
APP_VERSION = "1.0.0"


def get_environment():
    return os.getenv("ENVIRONMENT") or os.getenv("APP_ENV", "development")


# Prometheus metrics
http_requests = Counter(
    "http_requests_total",
    "Total HTTP requests received",
    ["method", "endpoint", "status"],
)

request_duration = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["endpoint"],
)

app_info = Gauge(
    "app_info",
    "Application version and environment",
    ["version", "environment"],
)

app_info.labels(
    version=APP_VERSION,
    environment=get_environment(),
).set(1)


@app.before_request
def start_request():
    g.start_time = time.perf_counter()


@app.after_request
def record_request(response):
    endpoint = request.path
    status = response.status_code

    duration = time.perf_counter() - g.start_time

    http_requests.labels(
        method=request.method,
        endpoint=endpoint,
        status=str(status),
    ).inc()

    request_duration.labels(
        endpoint=endpoint,
    ).observe(duration)

    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": "ERROR" if status >= 500 else "INFO",
        "message": "HTTP request completed",
        "endpoint": endpoint,
        "method": request.method,
        "status": status,
        "environment": get_environment(),
    }

    print(json.dumps(log_entry), flush=True)

    return response


# Original endpoints
@app.route("/health")
def health():
    return jsonify({"status": "UP"})


@app.route("/version")
def version():
    return jsonify({"version": APP_VERSION})


@app.route("/environment")
def environment():
    return jsonify({"environment": get_environment()})


# New Prometheus endpoint
@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        content_type=CONTENT_TYPE_LATEST,
    )


# Fault injection for incident testing
@app.route("/simulate-error")
def simulate_error():
    enabled = os.getenv(
        "ENABLE_FAULT_INJECTION", "false"
    ).lower() == "true"

    if not enabled:
        return jsonify({"error": "Not found"}), 404

    return jsonify({"error": "Simulated server error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
