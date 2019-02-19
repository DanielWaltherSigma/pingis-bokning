import os
from flask import Flask, jsonify, send_from_directory, request
from flask_mail import Mail, Message
from db_connection.configuration import ip, mail_config
from helpers import ActivityEnum, get_status_helper, check_whether_to_notify
from database_models.models import *

# Set up
app = Flask(__name__, static_folder="build")
app.config.update(
    MAIL_SERVER=mail_config["server"],
    MAIL_PORT=mail_config["port"],
    MAIL_USE_SSL=mail_config["use_ssl"],
    MAIL_USERNAME=mail_config["username"],
    MAIL_PASSWORD=mail_config["password"],
    TESTING=True,
    TEMPLATES_AUTO_RELOAD=True
)
mail = Mail(app)


@app.route("/api/status", methods=['GET'])
def get_status():
    """
    Checks the latest status of our two activities
    :return: json with latest status and whether there are reservations
    """
    to_return = {
        "table_tennis": get_status_helper(ActivityEnum.TABLE_TENNIS.value),
        "fussball": get_status_helper(ActivityEnum.FUSSBALL.value)
    }

    return jsonify(to_return)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE, OPTIONS')
    return response


@app.route("/api/book", methods=["POST"])
def book_activity():
    data = request.get_json()
    activity = data["activity"]

    try:
        email = data["email"]
        status = get_status_helper(activity)
        if status["sensor_status_occupied"] or len(status["reserved_list"]) > 0:
            booking = Booking.create(activity=activity,
                                     email=email,
                                     expires=datetime.datetime.now() + datetime.timedelta(hours=4))
        else:
            booking = Booking.create(activity=activity,
                                     email=email,
                                     expires=datetime.datetime.now() + datetime.timedelta(minutes=5))
        to_return = {
            "activity": activity,
            "booking_successful": True,
            "expires": booking.expires
        }
        return jsonify(to_return)
    except KeyError:
        pass


@app.route("/api/sensor_data", methods=["POST"])
def handle_sensor_data():
    data = request.get_json()
    name = data["sensor_name"]
    occupied = data["occupied"]

    sensor_status = SensorStatus.update(name=name, occupied=occupied)
    activity = SensorLookup.select(SensorLookup.activity).where(SensorLookup.sensor == sensor_status.sensor_name)
    if occupied == 0:
        check_whether_to_notify(activity, mail)



@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def main(path):
    if path != "" and os.path.exists("build/" + path):
        return send_from_directory('build', path)
    else:
        return send_from_directory('build', 'index.html')


if __name__ == "__main__":

    app.run(debug=True, host=ip["address"])
