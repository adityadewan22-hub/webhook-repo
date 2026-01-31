from datetime import datetime
import logging
from db import events_collection

logger = logging.getLogger(__name__)


def store_event(action, author, from_branch, to_branch, request_id):
    """
    Persists a normalized GitHub event into the database.
    This function is intentionally small and focused so it can be reused
    across different webhook handlers.
    """

    try:
        event = {
            "request_id": request_id,
            "author": author,
            "action": action,
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": datetime.utcnow()
        }

        events_collection.insert_one(event)

    except Exception:
        # Log full traceback so failures are visible in production logs
        logger.exception("Failed to store event in database")
        raise
