from marshmallow import *

from models.db_models import SensorLookup


class BookActivitySchema(Schema):
    activity = fields.String(required=True)
    email = fields.Email(required=True)

    @post_load
    def check_activity(self, data):
        if data["activity"] not in [item.value for item in SensorLookup.ActivityEnum]:
            raise Exception("No such activity available")


