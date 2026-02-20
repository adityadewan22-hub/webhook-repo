import logging
from celery_app import celery
from services.event_service import store_event

logger = logging.getLogger(__name__)


@celery.task(bind=True, max_retries=3)
def store_event_task(self, action, author, from_branch, to_branch, request_id):
    """
    Background task to store GitHub event in database.
    Retries up to 3 times if DB fails.
    """
    try:
        store_event(
            action=action,
            author=author,
            from_branch=from_branch,
            to_branch=to_branch,
            request_id=request_id,
        )
        logger.info("Event stored successfully (async)")

    except Exception as e:
        logger.exception("Failed to store event. Retrying...")
        raise self.retry(exc=e, countdown=5)
