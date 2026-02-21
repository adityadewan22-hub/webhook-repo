from flask import Blueprint, request, jsonify
import logging
from services.tasks import store_event_task

webhook_bp = Blueprint("webhook", __name__)
logger = logging.getLogger(__name__)


@webhook_bp.route("/webhook", methods=["POST"])
def webhook():
    """
    Receives GitHub webhook events and persists relevant data.
    Handles push, pull request open, and pull request merge events.
    """

    try:
        # Identify the GitHub event type and unique delivery ID
        event_type = request.headers.get("X-GitHub-Event")
        request_id = request.headers.get("X-GitHub-Delivery")
        payload = request.json

        # ---------------- PUSH EVENT ----------------
        # Triggered when code is pushed to a branch
        if event_type == "push":
            author = payload.get("pusher", {}).get("name")
            ref = payload.get("ref")
            to_branch = ref.split("/")[-1] if ref else None

            store_event_task.delay(
                action="PUSH",
                author=author,
                from_branch=None,
                to_branch=to_branch,
                request_id=request_id,
            )

            logger.info("Stored PUSH event")

        # ---------------- PULL REQUEST EVENTS ----------------
        # Triggered when a pull request is opened or merged
        elif event_type == "pull_request":
            action = payload.get("action")
            pr = payload.get("pull_request", {})
            merged = pr.get("merged", False)

            author = pr.get("user", {}).get("login")
            from_branch = pr.get("head", {}).get("ref")
            to_branch = pr.get("base", {}).get("ref")

            # Pull request opened
            if action == "opened":
                store_event_task.delay(
                    action="PULL_REQUEST",
                    author=author,
                    from_branch=from_branch,
                    to_branch=to_branch,
                    request_id=request_id,
                )

                logger.info("Stored PULL_REQUEST event")

            # Pull request merged
            elif action == "closed" and merged:
                store_event_task.delay(
                    action="MERGE",
                    author=author,
                    from_branch=from_branch,
                    to_branch=to_branch,
                    request_id=request_id,
                )

                logger.info("Stored MERGE event")

            else:
                logger.info(f"Ignored pull request action: {action}")

        # Ignore unsupported GitHub events
        else:
            logger.info(f"Ignored event type: {event_type}")

        # Always acknowledge receipt so GitHub does not retry
        return jsonify({"status": "received"}), 200

    except Exception as e:
        # Log full traceback for debugging and monitoring
        logger.exception("Error processing GitHub webhook")

        # Return 500 so GitHub may retry delivery
        return jsonify({"error": "Failed to process webhook"}), 500
