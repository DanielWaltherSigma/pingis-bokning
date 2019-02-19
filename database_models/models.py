import datetime

from db_connection.db_connection import BaseModel
from peewee import *


class SensorStatus(BaseModel):
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
    id = PrimaryKeyField()
    sensor = ForeignKeyField(SensorStatus, to_field=SensorStatus.sensor_name)
    activity = CharField()

