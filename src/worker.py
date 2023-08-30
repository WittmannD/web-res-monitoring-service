from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger, get_logger

from src.app import create_worker_app
from src.tasks.monitoring import fetch_monitors

logger = get_logger(__name__)
task_logger = get_task_logger(__name__)


def create_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["BROKER_URL"],
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


flask_app = create_worker_app()
celery_app = create_celery(flask_app)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/5'), fetch_monitors.s(), name="check monitors every 5m")
