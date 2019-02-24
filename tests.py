import unittest
from datetime import datetime, timedelta, date

import peewee

from handling import get_status, make_booking
from models.db_models import SensorStatus, SensorLookup, Booking

MODELS = [SensorStatus, SensorLookup, Booking]

test_db = peewee.SqliteDatabase(':memory:')


class TestCaseWithPeewee(unittest.TestCase):

    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def add_dummy_data(self):
        SensorStatus.create(sensor_name="dummy_sensor_1", occupied=True)
        SensorStatus.create(sensor_name="dummy_sensor_2", occupied=False)
        SensorStatus.create(sensor_name="dummy_sensor_3", occupied=False, timestamp=date.today() - timedelta(1))
        SensorStatus.create(sensor_name="dummy_sensor_4", occupied=False, timestamp=date.today() - timedelta(2))

        Booking.create(activity=SensorLookup.ActivityEnum.TABLE_TENNIS.value,
                       email="joel@example.com",
                       expires=datetime.now() - timedelta(days=2))
        Booking.create(activity=SensorLookup.ActivityEnum.TABLE_TENNIS.value,
                       email="alex@example.com",
                       expires=datetime.now() + timedelta(days=1))

        SensorLookup.create(sensor="dummy_sensor_1",
                            activity=SensorLookup.ActivityEnum.TABLE_TENNIS.value)

        SensorLookup.create(sensor="dummy_sensor_2",
                            activity=SensorLookup.ActivityEnum.TABLE_TENNIS.value)

        SensorLookup.create(sensor="dummy_sensor_3",
                            activity=SensorLookup.ActivityEnum.FUSSBALL.value)

        SensorLookup.create(sensor="dummy_sensor_4",
                            activity=SensorLookup.ActivityEnum.FUSSBALL.value)

    def test_sensor_lookup(self):
        self.add_dummy_data()
        sensor_1 = SensorStatus.get(SensorStatus.sensor_name == "dummy_sensor_1")
        self.assertEqual(sensor_1.sensor_name, "dummy_sensor_1")
        self.assertEqual(sensor_1.occupied, True)

    def test_get_sensor_status(self):
        self.add_dummy_data()
        status = get_status(SensorLookup.ActivityEnum.TABLE_TENNIS.value)
        self.assertEqual(status["sensor_status_occupied"], True)
        self.assertEqual(1, len(status["reservations_list"]))

        # Get Fussball status
        status = get_status(SensorLookup.ActivityEnum.FUSSBALL.value)
        self.assertEqual(False, status["sensor_status_occupied"])

    def test_make_reservation(self):
        self.add_dummy_data()
        old_len = len(list(Booking.select().where(Booking.expires > datetime.now())))
        # Make new reservation for table tennis where there already is a reservation
        new_booking_data = {
            "activity": "table_tennis",
            "email": "anders@apa.com"
        }
        booking_info = make_booking(new_booking_data)
        print(booking_info)
        new_len = len(list(Booking.select().where(Booking.expires > datetime.now())))
        self.assertEqual(old_len + 1, new_len)


    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection...but a good practice all the same.
        test_db.drop_tables(MODELS)

        # Close connection to db.
        test_db.close()


