from flask import Blueprint, jsonify
from db import events_collection
import logging
from datetime import datetime

events_bp = Blueprint("events", __name__)
logger = logging.getLogger(__name__)

## finds and sorts events by latest events

@events_bp.route("/events", methods=["GET"])
def get_events():
    try:
        minutes_15_ago=datetime.now()-15*60*1000
        events = list(
            events_collection
            .find(
                {"timestamp":{"$gte":minutes_15_ago}},
                {"_id": 0})
            .sort("timestamp", -1)
        )

        return jsonify(events), 200

    except Exception as e:
        logger.exception("Failed to fetch events")
        return jsonify({"error": "Failed to fetch events"}), 500
