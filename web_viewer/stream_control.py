import subprocess

# Stop
STOP_STREAM_SCRIPT="/home/pi/.modbus_converter/rpi_stop_video_stream.sh"
STOP_WEB_STREAM_SCRIPT="/home/pi/.modbus_converter/web_viewer/stream_scripts/camera_stop_webstream_server.sh"

# New resolution
SET_RES_1920X1080_SCRIPT="/home/pi/.modbus_converter/web_viewer/stream_scripts/camera_set_resolution_1920x1080.sh"
SET_RES_4k_SCRIPT="/home/pi/.modbus_converter/web_viewer/stream_scripts/camera_set_resolution_4k.sh"

# Streams
RUN_1080P_WEB_STREAM_SCRIPT="/home/pi/.modbus_converter/web_viewer/stream_scripts/webstream"

def stream_helper_stop_stream():
    subprocess.call(STOP_STREAM_SCRIPT)
    subprocess.call(STOP_WEB_STREAM_SCRIPT)

def stream_helper_set_resolution(resolution):
    if resolution == "1080p":
        subprocess.call(SET_RES_1920X1080_SCRIPT)
    elif resolution == "4k":
        subprocess.call(SET_RES_4k_SCRIPT)

def stream_helper_run(resolution):
    subprocess.Popen(["python", RUN_1080P_WEB_STREAM_SCRIPT, resolution])
