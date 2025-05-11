import os
from celery import Celery

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,

    # Worker settings
    worker_concurrency=4,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    task_reject_on_worker_lost=True,

    # Priority + Retry safety
    task_queue_max_priority=10,
    broker_connection_retry_on_startup=True,

    # Routing
    task_routes={
        "tasks.process_task": {"queue": "default"},
        "tasks.handle_dead_letter_task": {"queue": "dlq"},
    },

    task_queues={
        "default": {
            "exchange": "default",
            "routing_key": "default",
        },
        "dlq": {
            "exchange": "dlq",
            "routing_key": "dlq",
        },
    },

    # Optional: handle unroutable tasks
    task_default_queue="default",
    task_default_exchange="default",
    task_default_routing_key="default",
)
