from datetime import datetime
from db import events_collection

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
