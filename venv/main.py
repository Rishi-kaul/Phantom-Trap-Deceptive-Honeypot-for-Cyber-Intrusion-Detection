from flask import Flask, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Allow frontend to access backend

# Load logs from Cowrie (Modify the path based on your setup)
def load_logs():
    try:
        with open("/opt/cowrie/log/cowrie.json", "r") as file:
            return [json.loads(line) for line in file.readlines()]
    except FileNotFoundError:
        return []

@app.route("/api/logs", methods=["GET"])
def get_logs():
    logs = load_logs()
    parsed_logs = [{
        "timestamp": log["timestamp"],
        "ip": log.get("src_ip", "Unknown"),
        "username": log.get("username", "Unknown"),
        "password": log.get("password", "Unknown")
    } for log in logs if "login_attempt" in log]
    return jsonify(parsed_logs)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
