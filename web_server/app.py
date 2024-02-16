#!/usr/bin/env python
import os
import sys
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    jsonify,
    Response
)
from werkzeug.exceptions import (
    default_exceptions,
    HTTPException,
    InternalServerError
)
from helpers import (
    helper_get_my_ip,
    helper_update_host_ip_config
)
from modbus import (
    modbus_connect_to_tcp_rtu_converter,
    modbus_get_battery_level,
    modbus_focus_motor_control,
    modbus_light_control,
    modbus_main_motors_control
)
import stream_control as stream
import config_reader as conf_reader
import signal

app = Flask(__name__)

# Load main page #
##################
@app.route("/", methods=["GET"])
def index():
    ip = helper_get_my_ip()

    print("Board ip=" + ip)
    print("Client ip=" + request.remote_addr)

    # Gstream launch scripts will use this file to define host IP address to send stream
    helper_update_host_ip_config(request.remote_addr)
    sys.stdout.flush()

    return render_template('index.html', board_ip=ip)


# AJAX: Handle video buttons #
##############################
@app.route("/video_control", methods=["GET", "POST"])
def resolution_switch_request():
    print("Obtained request to change stream resolution to " + request.args.get("new_res"))

    stream.stop_stream()
    stream.set_resolution(request.args.get("new_res"))
    sys.stdout.flush()

    return jsonify("OK")


# STREAM: send jpeg frame #
###########################
def get_camera_frame():
    while True:
        # stream.capture_image()
        with open(stream.get_img_path(), 'rb') as f:
            frame = f.read()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(get_camera_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


# AJAX: Focus change via Modbus #
#################################
@app.route("/focus_control", methods=["GET", "POST"])
def focus_control_request():
    print("Obtained request to focus " + request.args.get("sign"))

    # Call Modbus TCP/RTU converter to send focus cmd and wait for reply
    modbus_focus_motor_control(request.args.get("sign"))
    sys.stdout.flush()

    return jsonify("OK")


# AJAX: Light control via Modbus #
##################################
@app.route("/light_control", methods=["GET", "POST"])
def light_control_request():
    print("Obtained request to make light " + request.args.get("level"))

    # Call Modbus TCP/RTU converter to send light cmd and wait for reply
    modbus_light_control(request.args.get("level"))
    sys.stdout.flush()

    return jsonify("OK")


# AJAX: up/left/right/down + WORK/STOP/HOME control via Modbus #
###########################################################
@app.route("/motor_control", methods=["GET", "POST"])
def motor_control_request():
    print("Obtained request to move motors to " + request.args.get("position"))

    # Call Modbus TCP/RTU converter to send position cmd and wait for reply
    modbus_main_motors_control(request.args.get("position"))
    sys.stdout.flush()

    return jsonify("OK")


# AJAX: Get battery level via Modbus #
######################################
@app.route("/get_battery_level", methods=["GET", "POST"])
def get_battery_level_request():
    print("Obtained request to retrieve battery level")

    # Call Modbus TCP/RTU converter and wait for reply
    level = modbus_get_battery_level()
    sys.stdout.flush()

    return jsonify({ "level": level })


# AJAX: Get config #
####################
@app.route("/get_conf", methods=["GET", "POST"])
def send_config_data_to_client():
    soc_pol_time = conf_reader.get_soc_polling_period_ms()
    repeat_cmds = conf_reader.get_repeat_cmd_perid_ms()
    initial_bat_level = modbus_get_battery_level()
    sys.stdout.flush()

    return jsonify({ "modbus_soc_polling_period_ms":  soc_pol_time,
                     "modbus_repeat_cmd_period_ms": repeat_cmds,
                      "initial_bat_level": initial_bat_level })


# Cathing internal sever error #
################################
@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    print(e)
    return redirect("/")

if __name__ == '__main__':
    # Ignore SIGCHLD to avoid zombi-proccesses
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    # Enable debug mode?
    if conf_reader.is_debug_enabled() == "On":
        print("Debug mode ENABLED")
        debug_mode = True
    else:
        print("Debug mode DISABLED")
        debug_mode = False

    # Connect to modbus TCP/RTU deamon
    modbus_connect_to_tcp_rtu_converter(debug_mode)

    # Temp file to save one frame
    if not os.path.exists(stream.get_img_path()):
        with open(stream.get_img_path(), 'w'):
            pass

    # Disable previously enabled settings
    stream.stop_stream()
    stream.set_resolution("1080p")
    sys.stdout.flush()

    # run server
    app.run(host='0.0.0.0', debug=debug_mode)