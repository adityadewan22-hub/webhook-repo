from flask import Flask, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import os
import logging

# -------------------- SETUP --------------------
load_dotenv()

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------- MONGO --------------------
client = MongoClient(os.getenv("MONGO_URI"))
db = client["github_events"]
events_collection = db["events"]

# -------------------- HELPERS ------------------
def store_event(action, author, from_branch, to_branch, request_id):
    event = {
        "request_id": request_id,
        "author": author,
        "action": action,
        "from_branch": from_branch,
        "to_branch": to_branch,
        "timestamp": datetime.utcnow()
    }
    events_collection.insert_one(event)

# -------------------- ROUTES -------------------
@app.route("/", methods=["GET"])
def health():
    return "OK", 200


@app.route("/events", methods=["GET"])
def get_events():
    events = list(
        events_collection.find({}, {"_id": 0}).sort("timestamp", -1)
    )
    return jsonify(events), 200


@app.route("/webhook", methods=["POST"])
def webhook():
    event_type = request.headers.get("X-GitHub-Event")
    request_id = request.headers.get("X-GitHub-Delivery")
    payload = request.json

    # ---------- PUSH ----------
    if event_type == "push":
        author = payload.get("pusher", {}).get("name")
        ref = payload.get("ref")
        to_branch = ref.split("/")[-1] if ref else None

        store_event(
            action="PUSH",
            author=author,
            from_branch=None,
            to_branch=to_branch,
            request_id=request_id
        )

        logger.info("STORED EVENT: PUSH")

    # ---------- PULL REQUEST / MERGE ----------
    elif event_type == "pull_request":
        action = payload.get("action")
        pr = payload.get("pull_request", {})
        merged = pr.get("merged", False)

        author = pr.get("user", {}).get("login")
        from_branch = pr.get("head", {}).get("ref")
        to_branch = pr.get("base", {}).get("ref")

        # PR OPENED
        if action == "opened":
            store_event(
                action="PULL_REQUEST",
                author=author,
                from_branch=from_branch,
                to_branch=to_branch,
                request_id=request_id
            )
            logger.info("STORED EVENT: PULL_REQUEST")

        # PR MERGED
        elif action == "closed" and merged is True:
            store_event(
                action="MERGE",
                author=author,
                from_branch=from_branch,
                to_branch=to_branch,
                request_id=request_id
            )
            logger.info("STORED EVENT: MERGE")

        else:
            logger.info(f"IGNORED PR EVENT: {action}")

    else:
        logger.info(f"IGNORED EVENT TYPE: {event_type}")

    return jsonify({"status": "received"}), 200


# -------------------- ENTRY --------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
