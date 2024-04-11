import re
import subprocess
import logging
from time import sleep
import threading


class VideoStreamer:
    # Stop gstreamer and v4l2 if running
    STOP_STREAM_SCRIPT_FILE_PATH="/home/pi/.microscope/scripts/rpi_stop_video_stream.sh"

    # Set resolution
    SET_RES_1920X1080_SCRIPT_FILE_PATH="/home/pi/.microscope/web_server/stream_scripts/camera_set_resolution_1920x1080.sh"
    SET_RES_4k_SCRIPT_FILE_PATH="/home/pi/.microscope/web_server/stream_scripts/camera_set_resolution_4k.sh"

    # Get exactly one frame
    GET_JPEG_IMG_FRAME_SCRIPT_FILE_PATH="/home/pi/.microscope/web_server/stream_scripts/camera_capture_one_image_frame.sh"
    
    # Get frames in continuously mode (for threading)
    START_JPEG_IMG_FRAME_CONTINUOUSLY_SCRIPT_FILE_PATH="/home/pi/.microscope/web_server/stream_scripts/camera_capture_frames_continuously.sh"

    is_stream_started_flag = False
    is_stop_pending_flag = False
    is_stop_done_flag = False

    last_captured_frame = b''

    current_width = "1920"
    current_height = "1080"
    current_framerate = "30"

    # Lock to access self.last_captured_frame
    mutex = threading.Lock()


    def __init__(self):
        subprocess.call(self.STOP_STREAM_SCRIPT_FILE_PATH)
        subprocess.call(self.SET_RES_1920X1080_SCRIPT_FILE_PATH)
        self.cam_device_connected()

    def cam_device_connected(self):
        device_re = re.compile(b"Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
        df = subprocess.check_output("lsusb")
        devices = []
        for i in df.split(b'\n'):
            if i:
                info = device_re.match(i)
                if info:
                    dinfo = info.groupdict()
                    dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                    devices.append(dinfo)

        if str(devices).find("16MP Camera Mamufacture 16MP USB Camera") == -1:
            logging.info("USB Camera not found")
        else:
            logging.info("USB CAMERA CONNECTED")

            self.pipe = subprocess.Popen([self.START_JPEG_IMG_FRAME_CONTINUOUSLY_SCRIPT_FILE_PATH, self.current_width, self.current_height, self.current_framerate], stdout=subprocess.PIPE, bufsize=-1)
            logging.info("Start read stdout from Gstreamer")

            self.thread = threading.Thread(target=self.mjpg_frames_fetcher, args=())
            self.thread.start()
            self.is_stream_started_flag = True
            self.is_stop_done_flag = False
            self.is_stop_pending_flag = False
            logging.info("Create new mjpg fetcher thread")


    def cam_device_disconnected(self):
        device_re = re.compile(b"Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
        df = subprocess.check_output("lsusb")
        devices = []
        for i in df.split(b'\n'):
            if i:
                info = device_re.match(i)
                if info:
                    dinfo = info.groupdict()
                    dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                    devices.append(dinfo)

        if str(devices).find("16MP Camera Mamufacture 16MP USB Camera") == -1:
            subprocess.call(self.STOP_STREAM_SCRIPT_FILE_PATH)
            self.request_to_stop_mjpg_fetcher()
            self.wait_stopping()
            logging.info("USB CAMERA HAS BEEN DISCONNECTED")
        else:
            logging.info("USB camera is still connected")


    def mjpg_frames_fetcher(self):
        bytes = b''
        while True:
            part = self.pipe.stdout.read(10000)
            bytes += part
            a = bytes.find(b'\xff\xd8')
            b = bytes.find(b'\xff\xd9')
            if a != -1 and b != -1:
                self.mutex.acquire()
                self.last_captured_frame = bytes[a:b+2]
                self.mutex.release()
                bytes = bytes[b+2:]

            if self.is_stop_pending_flag:
                self.is_stop_done_flag = True
                self.is_stream_started_flag = False
                self.is_stop_pending_flag = False
                logging.info("Video fetcher has been stopped")
                break


    def request_to_stop_mjpg_fetcher(self):
        self.is_stop_pending_flag = True
        self.is_stop_done_flag = False
        logging.debug("Video streaming request to stop mjpg fetcher thread..")


    def wait_stopping(self):
        stop_iter = 0
        logging.debug("Video streaming waiting stop.....")
        if self.is_stream_started_flag:
            while self.is_stop_done_flag == False:
                sleep(0.1)
                stop_iter += 1
                if stop_iter >= 40: # 4sec
                    break
            sleep(0.5)
        logging.debug("Video streaming waiting stop done")


    def set_resolution(self, resolution):
        if resolution == "1080p" and self.current_width == "1920" or resolution == "4k" and self.current_width == "4656":
            logging.info("Requested resolution {} had already been set previously".format(resolution))
            return
        else:
            logging.info("Video streamer obtained request to change stream resolution to " + resolution)

        self.request_to_stop_mjpg_fetcher()
        self.wait_stopping()
        sleep(0.1)
        subprocess.call(self.STOP_STREAM_SCRIPT_FILE_PATH)
        sleep(0.1)

        if resolution == "1080p":
            subprocess.call(self.SET_RES_1920X1080_SCRIPT_FILE_PATH)
            self.current_width = "1920"
            self.current_height = "1080"
            self.current_framerate = "30"
        elif resolution == "4k":
            subprocess.call(self.SET_RES_4k_SCRIPT_FILE_PATH)
            self.current_width = "4656"
            self.current_height = "3496"
            self.current_framerate = "10"
        else:
            logging.error("Video streamer wrong command to set resolution")
            return

        # Create pipe and thread again
        self.pipe = subprocess.Popen([self.START_JPEG_IMG_FRAME_CONTINUOUSLY_SCRIPT_FILE_PATH, self.current_width, self.current_height, self.current_framerate], stdout=subprocess.PIPE, bufsize=10**8)
        self.thread = threading.Thread(target=self.mjpg_frames_fetcher, args=())
        self.thread.start()
        logging.info("Start video fetching and streaming")
        self.is_stream_started_flag = True
        self.is_stop_done_flag = False
        self.is_stop_pending_flag = False

    def capture_frame(self):
        self.mutex.acquire()
        frame = self.last_captured_frame
        self.mutex.release()

        return frame
