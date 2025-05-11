import time
import logging
import json
from datetime import datetime
from contextlib import contextmanager
  
from celery import Task as CeleryTask
from celery.exceptions import MaxRetriesExceededError

from database import get_db
from celery_app import celery_app
from models import UserTask, UserTaskStatus, DeadLetteredTask

logger = logging.getLogger(__name__)

MAX_RETRIES = 3

class DatabaseTask(CeleryTask):
    abstract = True
    _db = None

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # Put the failed task in the dead letter queue for later processing
        handle_dead_letter_task.delay(task_id, args, kwargs, str(exc))
        logger.error(f"Task {task_id} failed after {MAX_RETRIES} retries, sending to DLQ, exc: {exc}")
        
@celery_app.task(
    base=DatabaseTask,
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={'max_retries': MAX_RETRIES},
    default_retry_delay=2,
)
def process_task(self, task_id: int):
    try:
        logger.info(f"Processing task {task_id}")
        with get_db() as db:
            task = db.query(UserTask).filter(UserTask.task_id == task_id).first()
            if not task:
                raise ValueError(f'Task {task_id} not found')
            
            # Process task logic here
            logger.info(f"Task {task_id} processing started")
            task.status = UserTaskStatus.in_progress
            db.commit()

            # Simulate work
            time.sleep(5)

            task.status = UserTaskStatus.completed
            db.commit()
            logger.info(f"Task {task_id} processed successfully")
            
    except Exception as exc:
        try:
            self.retry(exc=exc)
            logger.warning(f"Retrying task {task_id} due to: {exc}")
        except MaxRetriesExceededError as retry_exc:
            raise exc  # so that on_failure is called

@celery_app.task()
def handle_dead_letter_task(celery_task_id: str, args: list, kwargs: dict, error: str):

    with get_db() as db:
        db.add(
            DeadLetteredTask(
                celery_task_id=celery_task_id,
                args=json.dumps(args),
                kwargs=json.dumps(kwargs),
                error=str(error)
            )
        )
        db.commit()
        logger.info(f"Celery task id {celery_task_id} added to dead letter queue")