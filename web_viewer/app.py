from flask import Flask, redirect, render_template, request, session, jsonify
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

from helpers import helper_get_my_ip, helper_update_host_ip_config
from stream_control import stream_helper_stop_stream

app = Flask(__name__)
test_bat_level = 0

# Load main page #
##################
@app.route("/", methods=["GET"])
def index():
    ip = helper_get_my_ip()

    print("Board ip=" + ip)
    print("Client ip=" + request.remote_addr)

    # Gstream launch scripts will use this file to define host IP address to send stream
    helper_update_host_ip_config(request.remote_addr)
    return render_template('index.html', board_ip=ip)


# AJAX: Handle video buttons #
##############################
@app.route("/video_control", methods=["GET", "POST"])
def resolution_switch_request():
    print("Obtained request to change stream resolution to " + request.args.get("new_res"))

    stream_helper_stop_stream()
    return jsonify("OK")


# AJAX: Focus change via Modbus #
#################################
@app.route("/focus_control", methods=["GET", "POST"])
def focus_control_request():
    print("Obtained request to focus " + request.args.get("sign"))

    # Call Modbus TCP/RTU converter to send focus cmd and wait for reply
    return jsonify("OK")


# AJAX: Light control via Modbus #
##################################
@app.route("/light_control", methods=["GET", "POST"])
def light_control_request():
    print("Obtained request to make light " + request.args.get("level"))

    # Call Modbus TCP/RTU converter to send light cmd and wait for reply
    return jsonify("OK")


# AJAX: Up/left/right/down + STOP/HOME control via Modbus #
###########################################################
@app.route("/motor_control", methods=["GET", "POST"])
def motor_control_request():
    print("Obtained request to move motors to " + request.args.get("position"))

    # Call Modbus TCP/RTU converter to send position cmd and wait for reply
    return jsonify("OK")


# AJAX: Get battery level via Modbus #
#################################
@app.route("/get_battery_level", methods=["GET", "POST"])
def get_battery_level_request():
    print("Obtained request to retrieve battery level")

    # Call Modbus TCP/RTU converter and wait for reply
    global test_bat_level
    test_bat_level += 1
    if test_bat_level > 100:
        test_bat_level = 0
    
    json = {
        "level": str(test_bat_level)
    }
    return jsonify(json)


# Cathing internal sever error #
################################
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()

    print(e)
    return redirect("/")

for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
