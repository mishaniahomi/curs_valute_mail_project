from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.management import call_command
from curs.tasks import get_curs_now as gtn

logger = get_task_logger(__name__)


@shared_task
def sample_task():
    logger.info("The sample task just ran.")


@shared_task
def send_email_report():
    logger.info("d_email_reportsend_email_report")


@shared_task
def get_curs_now():
    gtn()
    logger.info("get curs now")