from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

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
    return jsonify({"status": "received"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
