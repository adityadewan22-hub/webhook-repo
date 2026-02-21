import os
from celery import Celery

# Redis URL
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery = Celery(
    "webhook_worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

# for tasks to be discovered
import services.tasks
