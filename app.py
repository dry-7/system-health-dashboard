import os
from flask import Flask, jsonify

app = Flask(__name__)

APP_VERSION = "1.0.0"


@app.route("/health")
def health():
    return jsonify({"status": "UP"})


@app.route("/version")
def version():
    return jsonify({"version": APP_VERSION})


@app.route("/environment")
def environment():
    env = os.getenv("APP_ENV", "development")
    return jsonify({"environment": env})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
