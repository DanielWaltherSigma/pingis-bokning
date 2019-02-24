from models.db_models import *
from datetime import date, timedelta, datetime
from handling import ActivityEnum


def recreate_tables():
    Booking.drop_table()
    SensorLookup.drop_table()
    SensorStatus.drop_table()

    SensorStatus.create_table()
    Booking.create_table()
    SensorLookup.create_table()


def create_tables():
    SensorStatus.create_table()
    Booking.create_table()
    SensorLookup.create_table()


if SensorStatus.table_exists():
    recreate_tables()
else:
    create_tables()

SensorStatus.create(sensor_name="dummy_sensor_1", occupied=True)
SensorStatus.create(sensor_name="dummy_sensor_2", occupied=False)
SensorStatus.create(sensor_name="dummy_sensor_3", occupied=False, timestamp=date.today() - timedelta(1))
SensorStatus.create(sensor_name="dummy_sensor_4", occupied=False, timestamp=date.today() - timedelta(2))

Booking.create(activity=ActivityEnum.TABLE_TENNIS.value,
               email="joel@example.com",
               expires=datetime.now() - timedelta(days=2))
Booking.create(activity=ActivityEnum.TABLE_TENNIS.value,
               email="alex@example.com",
               expires=datetime.now() + timedelta(days=1))

SensorLookup.create(sensor="dummy_sensor_1",
                    activity=ActivityEnum.TABLE_TENNIS.value)

SensorLookup.create(sensor="dummy_sensor_2",
                    activity=ActivityEnum.TABLE_TENNIS.value)

SensorLookup.create(sensor="dummy_sensor_3",
                    activity=ActivityEnum.FUSSBALL.value)

SensorLookup.create(sensor="dummy_sensor_4",
                    activity=ActivityEnum.FUSSBALL.value)
