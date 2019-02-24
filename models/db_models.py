import datetime
from enum import Enum

from db_connection.db_connection import BaseModel
from peewee import *


class SensorStatus(BaseModel):
    class SensorNamesEnum(Enum):
        TABLE_TENNIS_1 = "table-tennis-1"
        TABLE_TENNIS_2 = "table-tennis-2"
        FUSSBALL_1 = "fussball-1"
        FUSSBALL_2 = "fussball-2"

    sensor_name = CharField(null=False, index=True)
    occupied = BooleanField(null=False)
    timestamp = DateTimeField(default=datetime.datetime.now())


class Booking(BaseModel):
    id = PrimaryKeyField()
    activity = CharField()
    email = CharField()
    created = DateTimeField(default=datetime.datetime.now())
    expires = DateTimeField()


class SensorLookup(BaseModel):
    class ActivityEnum(Enum):
        TABLE_TENNIS = "table_tennis"
        FUSSBALL = "fussball"

    id = PrimaryKeyField()
    sensor = ForeignKeyField(SensorStatus, to_field=SensorStatus.sensor_name)
    activity = CharField()

