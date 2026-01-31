from flask import Blueprint, jsonify
from db import events_collection
import logging

events_bp = Blueprint("events", __name__)
logger = logging.getLogger(__name__)

## finds and sorts events by latest events

@events_bp.route("/events", methods=["GET"])
def get_events():
    try:
        events = list(
            events_collection
            .find({}, {"_id": 0})
            .sort("timestamp", -1)
        )

        return jsonify(events), 200

    except Exception as e:
        logger.exception("Failed to fetch events")
        return jsonify({"error": "Failed to fetch events"}), 500
