import subprocess

TEMP_IMG_FILE="/home/pi/.modbus_converter/web_viewer/tmp.img"

# Stop
STOP_STREAM_SCRIPT="/home/pi/.modbus_converter/rpi_stop_video_stream.sh"

# New resolution
SET_RES_1920X1080_SCRIPT="/home/pi/.modbus_converter/web_viewer/stream_scripts/camera_set_resolution_1920x1080.sh"
SET_RES_4k_SCRIPT="/home/pi/.modbus_converter/web_viewer/stream_scripts/camera_set_resolution_4k.sh"

# Obtain fdrame
GET_JPEG_FRAME_IMG_SCRIPT="/home/pi/.modbus_converter/web_viewer/stream_scripts/camera_capture_image.sh"

def stream_helper_stop_stream():
    subprocess.call(STOP_STREAM_SCRIPT)

def stream_helper_set_resolution(resolution):
    if resolution == "1080p":
        subprocess.call(SET_RES_1920X1080_SCRIPT)
    elif resolution == "4k":
        subprocess.call(SET_RES_4k_SCRIPT)

def stream_helper_capture_image():
    subprocess.call(GET_JPEG_FRAME_IMG_SCRIPT)

def stream_helper_get_img_path():
    return TEMP_IMG_FILE
