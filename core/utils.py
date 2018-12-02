from django.forms import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.core.mail import send_mail
from django.db.models import Model
from django.http import Http404

from airtech.settings import EMAIL_HOST_USER


class ExtendedEncoder(DjangoJSONEncoder):
    """
    Convert Django Model to JSON
    """

    def default(self, o):
        if isinstance(o, Model):
            return model_to_dict(o)

        return super().default(o)


def get_single_object(idx, obj_type):
    """
    Return a QuerySet object
    :param idx: Object ID
    :param obj_type: The Queryset Class
    :return: Queryset object
    """
    try:
        return obj_type.objects.get(id=idx)
    except obj_type.DoesNotExist:
        raise Http404


def send_flight_email(email=None, departure_city=None, departure_time=None, departure_date=None,
                      arrival_city=None, arrival_time=None, arrival_date=None, is_reminder=None):

    NEW_FLIGHT_SUBJECT = "Ticket Details for Trip: {} to {}"
    NEW_FLIGHT_MESSAGE = "Thank you for choosing to fly with us. Here are the details for your flight:" \
                         "Departure Time: {departure_time}, Departure City: {departure_city}, Departure Date: " \
                         "{departure_date}, Arrival Time: {arrival_time}, ArrivalCity: {arrival_city}, " \
                         "Arrival Date:{arrival_date} "
    REMINDER_SUBJECT = "Reminder for your flight to {} leaving tomorrow"
    REMINDER_MESSAGE = "Your flight to {departure_city} leaves tomorrow at {departure_time}. Here are the details:" \
                       "Departure Time: {departure_time}, Departure City: {departure_city}, Departure Date: " \
                       "{departure_date}, Arrival Time: {arrival_time}, ArrivalCity: {arrival_city}, " \
                       "Arrival Date:{arrival_date} "

    subject_params = (departure_city, arrival_city)
    message_params = {
        "departure_city": departure_city,
        "departure_time": departure_time,
        "departure_date": departure_date,
        "arrival_city": arrival_city,
        "arrival_time": arrival_time,
        "arrival_date": arrival_date
    }

    if is_reminder:
        subject = REMINDER_SUBJECT.format(*subject_params)
        message = REMINDER_MESSAGE.format(**message_params)
    else:
        subject = NEW_FLIGHT_SUBJECT.format(*subject_params)
        message = NEW_FLIGHT_MESSAGE.format(**message_params)

    send_mail(subject=subject, message=message, from_email=EMAIL_HOST_USER, recipient_list=[email])
