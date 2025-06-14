# web_logger.py
from flask import Flask, request
import json
from datetime import datetime

app = Flask(__name__)

LOG_FILE = "log.json"

@app.route("/", methods=["GET"])
def log_ip():
    visitor_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "user": "WEB_VISITOR",
        "message": f"IP: {visitor_ip} - Zaman: {now}"
    }

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(log_entry)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return "<h1>Hoş geldin!</h1><p>Giriş kaydın alındı 👀</p>", 200

if __name__ == "__main__":
    app.run(debug=True, port=8080)
