from flask import Blueprint, jsonify
from db import events_collection

events_bp = Blueprint("events", __name__)

# event for route, finds and sorts by latest events

@events_bp.route("/events", methods=["GET"])
def get_events():
    events = list(
        events_collection
        .find({}, {"_id": 0})
        .sort("timestamp", -1)
    )
    return jsonify(events), 200
