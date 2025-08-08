from flask_apscheduler import APScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

from Utils import update_availability
from src.logger import get_logger

logger = get_logger("scheduler")

scheduler = APScheduler()

def job_listener(event):
    if event.exception:
        logger.error(f"Job '{event.job_id}' failed: {event.exception}")
    else:
        logger.info(f"Job '{event.job_id}' executed successfully.")

def init_scheduler(app):
    scheduler.init_app(app)
    logger.info(f"Init success")
    # Wrap job to run inside app context
    def job_with_context():
        with app.app_context():
            update_availability()

    scheduler.add_job(
        id='update_availability',
        func=job_with_context,
        trigger='interval',
        minutes=9
    )

    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.start()
    logger.info("Scheduler started")
