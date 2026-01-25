from flask import Flask, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import logging

load_dotenv()

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- MongoDB connection ---
client = MongoClient(os.getenv("MONGO_URI"))
db = client["github_events"]
events_collection = db["events"]
# --------------------------


@app.route("/", methods=["GET"])
def health():
    return "OK", 200


@app.route("/test-db", methods=["POST"])
def test_db():
    test_event = {
        "test": "mongo_connection_working"
    }

    events_collection.insert_one(test_event)
    return jsonify({"status": "inserted"}), 200


@app.route("/events", methods=["GET"])
def get_events():
    events = list(events_collection.find({}, {"_id": 0}))
    return jsonify(events), 200


@app.route("/webhook", methods=["POST"])
def webhook():
    print("RAW EVENT HEADER:", request.headers.get("X-GitHub-Event"))

    event_type = request.headers.get("X-GitHub-Event")
    payload = request.json

    if event_type == "push":
        logger.info("EVENT DETECTED: PUSH")

    elif event_type == "pull_request":
        action = payload.get("action")
        merged = payload.get("pull_request", {}).get("merged", False)

        if action == "opened":
            print("EVENT DETECTED: PULL_REQUEST")

        elif action == "closed" and merged is True:
            print("EVENT DETECTED: MERGE")

        else:
            print(f"IGNORED PR EVENT: {action}")

    else:
        print(f"IGNORED EVENT TYPE: {event_type}")

    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

