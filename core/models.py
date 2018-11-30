import re

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


class Flight(models.Model):
    BOARDING = 'BO'
    DELAYED = 'DY'
    GOTOGATE = 'GTG'
    ONTIME = 'OT'
    FLIGHT_STATUS_CHOICES = (
        (BOARDING, 'Boarding'),
        (DELAYED, 'Delayed'),
        (GOTOGATE, 'Go To Gate'),
        (ONTIME, 'OT')
    )
    depature_time = models.TimeField()
    depature_date = models.DateField()
    depature_city = models.CharField(max_length=200)
    arrival_time = models.TimeField()
    arrival_date = models.DateField()
    arrival_city = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    status = models.CharField(
        max_length=3,
        choices=FLIGHT_STATUS_CHOICES,
        default=ONTIME
    )


class User(AbstractUser):
    date_of_birth = models.DateField(max_length=200, blank=True, null=True)
    photo = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.email

    def clean(self):
        password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        if self.password and not re.match(password_pattern, self.password):
            raise ValidationError(
                "Password must contain at least: "
                "1 upper case letter, 1 lower case letter, 1 special character, 1 digit "
                "and have a minimum 8 characters")

        email_pattern = "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}" \
                        "[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
        if self.email and not re.match(email_pattern, self.email):
            raise ValidationError("Invalid Email")


# Get custom model
UserModel = get_user_model()


class Ticket(models.Model):
    PURCHASED = 'PD'
    RESERVED = 'RD'
    FLIGHT_STATUS_CHOICES = (
        (PURCHASED, 'Purchased'),
        (RESERVED, 'Reserved'),
    )
    flight_details = models.ForeignKey(Flight, on_delete=models.CASCADE)
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    status = models.CharField(max_length=200)
