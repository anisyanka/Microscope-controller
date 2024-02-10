import subprocess

STOP_STREAM_SCRIPT="/home/pi/.modbus_converter/rpi_stop_video_stream.sh"

def stream_helper_stop_stream():
    rc = subprocess.call(STOP_STREAM_SCRIPT)
    return rc
