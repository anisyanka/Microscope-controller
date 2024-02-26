import subprocess
import logging
from time import sleep
import threading

class FrameGeneratorExit(Exception):
    """Exception to exit video cycle generator"""

class VideoStreamer:
    TEMP_IMG_FILE="/home/pi/.microscope/web_server/temp_img_frame"
    STOP_STREAM_SCRIPT_FILE_PATH="/home/pi/.microscope/scripts/rpi_stop_video_stream.sh"
    SET_RES_1920X1080_SCRIPT_FILE_PATH="/home/pi/.microscope/web_server/stream_scripts/camera_set_resolution_1920x1080.sh"
    SET_RES_4k_SCRIPT_FILE_PATH="/home/pi/.microscope/web_server/stream_scripts/camera_set_resolution_4k.sh"
    GET_JPEG_IMG_FRAME_SCRIPT_FILE_PATH="/home/pi/.microscope/web_server/stream_scripts/camera_capture_one_image_frame.sh"

    _is_stream_started = False

    _stop_pending = False
    _stop_done = False

    def __init__(self):
        subprocess.call(self.STOP_STREAM_SCRIPT_FILE_PATH)
        subprocess.call(self.SET_RES_1920X1080_SCRIPT_FILE_PATH)
        self.stream_to = "file"
        self.lock = threading.Lock()


    def request_to_start_stream(self):
        self.lock.acquire()
        self._is_stream_started = True
        self._stop_pending = False
        self._stop_done = False
        self.lock.release()
        logging.debug("Video streaming request to start")


    def is_stream_started(self):
        return self._is_stream_started


    def request_to_stop_stream(self):
        self.lock.acquire()
        self._stop_pending = True
        self._stop_done = False
        self.lock.release()
        logging.debug("Video streaming request to stop")


    def wait_stopping(self):
        stop_iter = 0
        logging.debug("Video streaming waiting stop.....")
        if self._is_stream_started:
            while self._stop_done == False:
                sleep(0.1)
                stop_iter += 1
                if stop_iter >= 40: # 4sec
                    break
        logging.debug("Video streaming waiting stop done")


    def set_resolution(self, resolution):
        self.request_to_stop_stream()
        self.wait_stopping()
        logging.debug("Video streamer obtained request to change stream resolution to " + resolution)
        if resolution == "1080p":
            subprocess.call(self.SET_RES_1920X1080_SCRIPT_FILE_PATH)
        elif resolution == "4k":
            subprocess.call(self.SET_RES_4k_SCRIPT_FILE_PATH)
        else:
            logging.error("Video streamer wrong command to set resolution")
        self.request_to_start_stream()


    def capture_frame(self):
        def _get_frame_from_file(self):
            with open(self.TEMP_IMG_FILE, 'rb') as f:
                frame = f.read()
            return frame

        if self._stop_pending: # return old frame
            if not self._stop_done:
                self.lock.acquire()
                subprocess.call(self.STOP_STREAM_SCRIPT_FILE_PATH)
                self._stop_done = True
                self._is_stream_started = False
                self.lock.release()

            if self.stream_to == "file":
                frame = _get_frame_from_file(self)
            elif self.stream_to == "pipe":
                pass
            else:
                logging.error("Specify proper stream_to for video streamer or use default constructor")
        else:
            if self.stream_to == "file":
                subprocess.call([self.GET_JPEG_IMG_FRAME_SCRIPT_FILE_PATH, self.TEMP_IMG_FILE])
                frame = _get_frame_from_file(self)
            elif self.stream_to == "pipe":
                pass
            else:
                logging.error("Specify proper stream_to for video streamer or use default constructor")

        return frame
