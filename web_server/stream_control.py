import subprocess

TEMP_IMG_FILE="/home/pi/.microscope/web_server/tmp.img"

# Stop
STOP_STREAM_SCRIPT="/home/pi/.microscope/scripts/rpi_stop_video_stream.sh"

# New resolution
SET_RES_1920X1080_SCRIPT="/home/pi/.microscope/web_server/stream_scripts/camera_set_resolution_1920x1080.sh"
SET_RES_4k_SCRIPT="/home/pi/.microscope/web_server/stream_scripts/camera_set_resolution_4k.sh"

# Obtain frame
GET_JPEG_FRAME_IMG_SCRIPT="/home/pi/.microscope/web_server/stream_scripts/camera_capture_image.sh"

def stop_stream():
    subprocess.call(STOP_STREAM_SCRIPT)

def set_resolution(resolution):
    if resolution == "1080p":
        subprocess.call(SET_RES_1920X1080_SCRIPT)
    elif resolution == "4k":
        subprocess.call(SET_RES_4k_SCRIPT)

def capture_image_frame():
    subprocess.call([GET_JPEG_FRAME_IMG_SCRIPT, TEMP_IMG_FILE])
    with open(TEMP_IMG_FILE, 'rb') as f:
        frame = f.read()
    return frame

def get_img_path():
    return TEMP_IMG_FILE
