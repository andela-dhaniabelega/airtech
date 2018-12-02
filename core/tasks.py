from datetime import datetime, timedelta

from celery.task import task
from celery.utils.log import get_task_logger

from core.models import Ticket
from core.utils import send_flight_email

logger = get_task_logger(__name__)


@task(name='Send Flight Reminder')
def send_flight_reminder_email_task():
    """
    Sends email to remind customers a day before their flight
    :return:
    """
    flight_date = datetime.now() + timedelta(days=1)
    for ticket in Ticket.objects.filter(flight_details__depature_date__day=flight_date.day):
        kwargs = {
            "departure_city": ticket.flight_details.depature_city,
            "departure_time": ticket.flight_details.depature_time,
            "departure_date": ticket.flight_details.depature_date,
            "arrival_city": ticket.flight_details.arrival_city,
            "arrival_time": ticket.flight_details.arrival_time,
            "arrival_date": ticket.flight_details.arrival_date,
            "email": ticket.owner.email
        }
        logger.info("Sent Reminder Email")
        return send_flight_email(**kwargs, is_reminder=True)


@task(name='Send Initial Ticket')
def send_initial_ticket_email_task(**kwargs):
    """
    Sends email to remind customers a day before their flight
    :return:
    """
    logger.info("Sent Initial Ticket")
    return send_flight_email(**kwargs)
