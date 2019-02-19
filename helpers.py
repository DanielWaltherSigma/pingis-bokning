import datetime
import json
from flask_mail import Mail, Message
from enum import Enum

from database_models.models import SensorLookup, SensorStatus, Booking


class ActivityEnum(Enum):
    TABLE_TENNIS = "table_tennis"
    FUSSBALL = "fussball"


class SensorNamesEnum(Enum):
    TABLE_TENNIS_1 = "table-tennis-1"
    TABLE_TENNIS_2 = "table-tennis-2"
    FUSSBALL_1 = "fussball-1"
    FUSSBALL_2 = "fussball-2"


def get_status_helper(activity):
    is_occupied = False
    emails = []

    if activity == ActivityEnum.TABLE_TENNIS.value:
        query = SensorLookup.select().where(SensorLookup.activity == ActivityEnum.TABLE_TENNIS.value)
        is_occupied = check_if_occupied(query)

        # Get reservations
        query = Booking.select().where(Booking.activity == ActivityEnum.TABLE_TENNIS.value,
                                       Booking.expires > datetime.datetime.now()
                                       or Booking.expires is None)

        reservation_list = list(query)
        emails = []
        for row in reservation_list:
            emails.append(row.email)
    elif activity == ActivityEnum.FUSSBALL.value:
        query = SensorLookup.select().where(SensorLookup.activity == ActivityEnum.FUSSBALL.value)

        is_occupied = check_if_occupied(query)

        query = Booking.select().where(Booking.activity == ActivityEnum.FUSSBALL.value,
                                       Booking.expires > datetime.datetime.now()
                                       or Booking.expires is None)

        reservation_list = list(query)
        emails = []
        for row in reservation_list:
            emails.append(row.email)

    return {
        "sensor_status_occupied": is_occupied,
        "reserved_list": emails
    }


def check_if_occupied(query):
    res = list(query)
    sensor_names = []
    for row in res:
        sensor_names.append(row.sensor.sensor_name)

    query = SensorStatus.select() \
        .where(SensorStatus.sensor_name == sensor_names[0]) \
        .limit(1)

    sensor_status = list(query)
    query = SensorStatus.select() \
        .where(SensorStatus.sensor_name == sensor_names[1]) \
        .limit(1)

    sensor_status.append(list(query)[0])
    is_occupied = False
    for row in sensor_status:
        if row.occupied:
            is_occupied = True
            break

    return is_occupied


def check_whether_to_notify(activity, mail):
    if activity == ActivityEnum.TABLE_TENNIS.value:
        query = Booking.select().where(Booking.activity == ActivityEnum.TABLE_TENNIS.value,
                                       Booking.expires > datetime.datetime.now()
                                       or Booking.expires is None)

        reservation_list = list(query)

        if len(reservation_list) > 0:
            next_booking = reservation_list[0]


def send_email(mail, email, activity):

        msg = Message(
            subject="It's your turn!",
            recipients=[email],
            body="The {} table is free. It is reserved for you for the next five minutes".format(activity)
        )
        mail.send(msg)

