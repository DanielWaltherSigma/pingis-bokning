import datetime
from flask_mail import Mail, Message

from models.db_models import SensorLookup, SensorStatus, Booking
from schemas import BookActivitySchema


def get_status(activity):
    is_occupied, emails = __get_status(activity)

    return {
        "sensor_status_occupied": is_occupied,
        "reservations_list": emails
    }

def __get_status(activity: str):
    query = SensorLookup.select().where(SensorLookup.activity == activity)
    res = list(query)
    is_occupied = check_if_occupied(query)

    # Get reservations
    query = Booking.select().where(Booking.activity == activity,
                                   Booking.expires > datetime.datetime.now()
                                   or Booking.expires is None)

    reservation_list = list(query)
    emails = []
    for row in reservation_list:
        emails.append(row.email)
    return is_occupied, emails

def check_if_occupied(query):
    """
    Checks both sensors associated with an activity
    If either indicates that there are people there now, returns that it's occupied
    :param query: Query from sensor lookup table
    :return: boolean of whether table is occupied
    """
    sensor_names = []
    for row in query:
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
    if activity == SensorLookup.ActivityEnum.TABLE_TENNIS.value:
        query = Booking.select().where(Booking.activity == SensorLookup.ActivityEnum.TABLE_TENNIS.value,
                                       Booking.expires > datetime.datetime.now()
                                       or Booking.expires is None)

        reservation_list = list(query)

        if len(reservation_list) > 0:
            next_booking = reservation_list[0]

def make_booking(data):
    # Load input data
    booking_schema = BookActivitySchema()
    checked_data = booking_schema.load(data).data
    activity = checked_data["activity"]
    email = checked_data["email"]

    status = get_status(activity)
    if status["sensor_status_occupied"] or len(status["reserved_list"]) > 0:
        # If table is booked, create a new long lasting reservation
        booking = Booking.create(activity=activity,
                                 email=email,
                                 expires=datetime.datetime.now() + datetime.timedelta(hours=4))
    else:
        # If table is free, book it now for five minutes
        booking = Booking.create(activity=activity,
                                 email=email,
                                 expires=datetime.datetime.now() + datetime.timedelta(minutes=5))

    to_return = {
        "activity": booking.activity,
        "booking_successful": True,
        "expires": booking.expires,
        "place_in_queue": len(list(Booking.select().where(Booking.expires > datetime.datetime.now())))
    }
    return to_return

def send_email(mail, email, activity):

        msg = Message(
            subject="It's your turn!",
            recipients=[email],
            body="The {} table is free. It is reserved for you for the next five minutes".format(activity)
        )
        mail.send(msg)

