from celery import group
from celery.utils.log import get_task_logger

from src.extensions import celery, db
from src.models.MonitorModel import MonitorModel
from src.tasks.Monitor import Monitor

logger = get_task_logger(__name__)


@celery.task
def check(data: dict):
    Monitor(data).check()


@celery.task
def fetch_monitors():
    period_sec = 60
    monitors = MonitorModel.get_pending(period_sec)

    if monitors is None or len(monitors) == 0:
        return

    logger.info(f'fetched {len(monitors)}')

    batch = group(check.s(monitor.as_json_serializable()) for monitor in monitors)
    batch()
