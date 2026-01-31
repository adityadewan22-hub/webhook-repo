from flask import Blueprint, request, jsonify
import logging
from services.event_service import store_event

webhook_bp = Blueprint("webhook", __name__)
logger = logging.getLogger(__name__)


## check for post webhook event

@webhook_bp.route("/webhook", methods=["POST"])
def webhook():
    event_type = request.headers.get("X-GitHub-Event")
    request_id = request.headers.get("X-GitHub-Delivery")
    payload = request.json

    if event_type == "push":
        author = payload.get("pusher", {}).get("name")
        ref = payload.get("ref")
        to_branch = ref.split("/")[-1] if ref else None

        store_event("PUSH", author, None, to_branch, request_id)

## check for pull_request webhook event

    elif event_type == "pull_request":
        action = payload.get("action")
        pr = payload.get("pull_request", {})
        merged = pr.get("merged", False)

        author = pr.get("user", {}).get("login")
        from_branch = pr.get("head", {}).get("ref")
        to_branch = pr.get("base", {}).get("ref")

        if action == "opened":
            store_event("PULL_REQUEST", author, from_branch, to_branch, request_id)
## check for pull_request.merged in payload

        elif action == "closed" and merged:
            store_event("MERGE", author, from_branch, to_branch, request_id)

    return jsonify({"status": "received"}), 200
