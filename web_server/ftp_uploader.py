import subprocess
import logging
from time import sleep
import threading
import config_reader as conf_reader
from enum import IntEnum

# On FTP server side the folder "Microscope_videos" will
# be created in ~/ directory. Inside that directories other directories named with <date_time>
# will be created. Inside those the videos will be saved.

# On the RPI side the same directories will be placed in
# "/home/pi/.microscope/videos" directory. After a video has been transferred, it will be removed from RPI.

video_root_dir_on_serv = "Microscope_videos"
video_root_dir_on_rpi = "/home/pi/.microscope/videos"


class FtpUploaderErrors(IntEnum):
    SUCCESS = 0,
    WRONG_IP_OR_PORT = 1,
    WRONG_USER_OR_PASS = 2,
    UNKNOWN_ERR = 3,
    FAILED_TO_CREATE_ROOT_VIDEO_DIR_ON_SERV = 4,
    FTP_CONNECTION_TIMEOUT = 5


class FtpUploader:
    # FTP scripts
    FTP_STOP_UPLOADING = "/home/pi/.microscope/web_server/ftp_scripts/stop_ftp_transfer.sh"
    FTP_CHECK_CONN = "/home/pi/.microscope/web_server/ftp_scripts/check_conn.sh"
    FTP_CREATE_DIR_ON_SERV = "/home/pi/.microscope/web_server/ftp_scripts/create_dir_on_server.sh"
    FTP_IS_FILE_EXISTS_ON_SERV = "/home/pi/.microscope/web_server/ftp_scripts/does_file_exist_on_server.sh"
    FTP_IS_FILE_EXISTS_ON_SERV_IN_DIR = "/home/pi/.microscope/web_server/ftp_scripts/does_file_exist_on_server_in_dir.sh"
    FTP_UPLOAD_FILE = "/home/pi/.microscope/web_server/ftp_scripts/upload_to_server.sh"
    FTP_FIND_VIDEO_TO_TX = "/home/pi/.microscope/web_server/ftp_scripts/find_video_to_tx.sh"

    # FTP current state
    is_ftp_enabled = 0
    is_ftp_server_exists = 0
    is_ftp_root_dir_exists = 0
    is_ftp_thread_duty_started = 0

    # Global error state to pass to users
    uploader_error = FtpUploaderErrors.SUCCESS

    # FTP data
    ftp_ip = str()
    ftp_port = str()
    ftp_user = str()
    ftp_pass = str()

    ftp_timeout = 0

    def __init__(self):
        # FTP initial state
        self.is_ftp_enabled = 0
        self.is_ftp_server_exists = 0
        self.is_ftp_root_dir_exists = 0
        self.is_ftp_thread_duty_started = 0

        # Kill all curl instances
        self.stop_any_ftp_trasferring()

        # Read config file
        self.ftp_ip = conf_reader.get_ftp_ip()
        self.ftp_port = conf_reader.get_ftp_port()
        self.ftp_user = conf_reader.get_ftp_user()
        self.ftp_pass = conf_reader.get_ftp_pass()

        # During initialization timeout is 1 sec.
        self.ftp_timeout = 1

        # Check the FTP server exists
        self.check_does_ftp_server_exist()

        # Check root dir for videos on server
        self.create_root_video_dir_if_doesnt_exist()

        # After server was running - 5 sec
        self.ftp_timeout = 5

        self.thread = threading.Thread(target=self.ftp_uploader_thread, args=())
        self.thread.start()
        logging.info("Create new FTP uploader thread")


    def update_configs(self):
        self.ftp_ip = conf_reader.get_ftp_ip()
        self.ftp_port = conf_reader.get_ftp_port()
        self.ftp_user = conf_reader.get_ftp_user()
        self.ftp_pass = conf_reader.get_ftp_pass()


    def stop_any_ftp_trasferring(self):
        subprocess.run(self.FTP_STOP_UPLOADING)
        sleep(1)
        subprocess.run(self.FTP_STOP_UPLOADING)


    def check_does_ftp_server_exist(self):
        """
        Return code = 1 - success, 
        Return code < 0 - fail. See self.get_last_err()
        """

        self.is_ftp_server_exists = 0
        try:
            out = subprocess.run([self.FTP_CHECK_CONN,
                                  self.ftp_user, self.ftp_pass,
                                  self.ftp_ip, self.ftp_port],
                                  capture_output=True,
                                  timeout=self.ftp_timeout)
            if out.stdout == b"0":
                logging.info(f"[FTP] check server. Connectoin to FTP {self.ftp_ip}:{self.ftp_port} as <{self.ftp_user}> SUCCESS")
                self.uploader_error = FtpUploaderErrors.SUCCESS
                self.is_ftp_server_exists = 1
                return 1
            elif out.stdout == b"7":
                logging.error("[FTP]  check server. Server is not running or wrong IP:PORT. Check server config file")
                self.uploader_error = FtpUploaderErrors.WRONG_IP_OR_PORT
                return -1
            elif out.stdout == b"67":
                logging.error("[FTP] check server. Failed to login. Check user and pass in config file")
                self.uploader_error = FtpUploaderErrors.WRONG_USER_OR_PASS
                return -2
            else:
                logging.error(f"[FTP] check server. Unknown error. rv={out.returncode}; stdout={out.stdout}; stderr={out.stderr}")
                self.uploader_error = FtpUploaderErrors.UNKNOWN_ERR
        except subprocess.TimeoutExpired as exp:
            logging.error(f"[FTP] check server. Connectoin to FTP {self.ftp_ip}:{self.ftp_port} as <{self.ftp_user}> - {exp}")
            self.uploader_error = FtpUploaderErrors.FTP_CONNECTION_TIMEOUT
            return -3

        return -4


    def create_root_video_dir_if_doesnt_exist(self):
        """
        Return code =  1 - exists or created, 
        Return code < 0 - fail to create. See self.get_last_err()
        """

        self.is_ftp_root_dir_exists = 0
        try:
            out = subprocess.run([self.FTP_IS_FILE_EXISTS_ON_SERV,
                                  self.ftp_user, self.ftp_pass,
                                  self.ftp_ip, self.ftp_port,
                                  video_root_dir_on_serv],
                                  capture_output=True,
                                  timeout=self.ftp_timeout)
            if out.stdout == b"0":
                logging.info(f"Root directory {self.ftp_ip}:{self.ftp_port}:~/{video_root_dir_on_serv} EXISTS")
                self.uploader_error = FtpUploaderErrors.SUCCESS
                self.is_ftp_root_dir_exists = 1
                return 1
            else:
                logging.info(f"Root directory {self.ftp_ip}:{self.ftp_port}:~/{video_root_dir_on_serv} DOES NOT EXIST. Try to create it")
                out = subprocess.run([self.FTP_CREATE_DIR_ON_SERV,
                                      self.ftp_user, self.ftp_pass,
                                      self.ftp_ip, self.ftp_port,
                                      video_root_dir_on_serv],
                                      capture_output=True,
                                      timeout=self.ftp_timeout)
                if out.stdout == b"0":
                    logging.info(f"Root directory {self.ftp_ip}:{self.ftp_port}:~/{video_root_dir_on_serv} CREATED")
                    self.uploader_error = FtpUploaderErrors.SUCCESS
                    return 1
                else:
                    logging.error(f"Root directory {self.ftp_ip}:{self.ftp_port}:~/{video_root_dir_on_serv} FAILED to create")
                    self.uploader_error = FtpUploaderErrors.FAILED_TO_CREATE_ROOT_VIDEO_DIR_ON_SERV
        except subprocess.TimeoutExpired as exp:
            logging.error(f"[FTP] check server. Connectoin to FTP {self.ftp_ip}:{self.ftp_port} as <{self.ftp_user}> - {exp}")
            self.uploader_error = FtpUploaderErrors.FTP_CONNECTION_TIMEOUT
            return -1

        return -2


    def get_last_err(self):
        return self.uploader_error


    def enable_ftp_transferring(self):
        """
        1 - success
        """

        logging.info("FTP enable request...")

        if self.is_ftp_enabled == 1:
            logging.info("FTP enabled")
            return 1

        if self.is_ftp_server_exists == 0:
            if self.check_does_ftp_server_exist() != 1:
                logging.error("FTP failed to enable. Can't login to server")
                return -1

        if self.is_ftp_root_dir_exists == 0:
            if self.create_root_video_dir_if_doesnt_exist() != 1:
                logging.error("FTP failed to enable. Can't create root dir for video")
                return -1

        self.is_ftp_enabled = 1
        return 1


    def disable_ftp_transferring(self):
        self.is_ftp_enabled = 0
        logging.info("FTP disabled request...")
        self.stop_any_ftp_trasferring()


    def is_ftp_transferring_enabled(self):
        return self.is_ftp_enabled


    def ftp_uploader_thread(self):
        while True:
            # Sleep here untill enable_ftp_transferring() call
            while self.is_ftp_enabled == 0:
                sleep(1)

            logging.info("[uploader] FTP start files uploading")
            while True:
                if self.is_ftp_enabled == 1:
                    sleep(1)

                    if self.is_ftp_enabled == 0:
                        break

                    # Find local dir with not yet uploaded videos and get video file and dir name
                    out = subprocess.run([self.FTP_FIND_VIDEO_TO_TX], capture_output=True)
                    dir_to_create = out.stdout.split()[0]
                    file_to_tx = out.stdout.split()[1]

                    logging.debug(f"[uploader] dir_to_create - {dir_to_create}, file_to_tx - {file_to_tx}")

                    if self.is_ftp_enabled == 0:
                        break

                    if dir_to_create != b"null" and file_to_tx != b"null":
                        newdir_abs_path = video_root_dir_on_serv + "/" + dir_to_create.decode("utf-8")

                        # Does directory exist on server? CWD to video_root_dir_on_serv
                        out = subprocess.run([self.FTP_IS_FILE_EXISTS_ON_SERV_IN_DIR,
                                              self.ftp_user, self.ftp_pass,
                                              self.ftp_ip, self.ftp_port,
                                              dir_to_create.decode("utf-8"),
                                              video_root_dir_on_serv], capture_output=True)

                        if self.is_ftp_enabled == 0:
                            break

                        if out.stdout != b"0":
                            logging.debug(f"[uploader] dir <{dir_to_create}> doesn't exist on server, so try to create it")

                            # Create due to not exists
                            out = subprocess.run([self.FTP_CREATE_DIR_ON_SERV,
                                                  self.ftp_user, self.ftp_pass,
                                                  self.ftp_ip, self.ftp_port,
                                                  newdir_abs_path], capture_output=True)
                            if out.stdout == b"0":
                                logging.info(f"[uploader] dir <{newdir_abs_path}> created on FTP server successfully")
                            else:
                                logging.error(f"[uploader] failed to create dir <{newdir_abs_path}> on FTP server")
                        else:
                            logging.debug(f"[uploader] dir <{dir_to_create}> already exists on FTP server")
                            pass
                    else:
                        # Local storage is fully empty or only the first file is being recording
                        continue

                    if self.is_ftp_enabled == 0:
                        break

                    # Upload video file
                    logging.info(f"[uploader] try to upload file <{file_to_tx}> to <{newdir_abs_path}> to FTP server")
                    out = subprocess.run([self.FTP_UPLOAD_FILE,
                                          self.ftp_user, self.ftp_pass,
                                          self.ftp_ip, self.ftp_port,
                                          video_root_dir_on_rpi + "/" + dir_to_create.decode("utf-8") + "/" + file_to_tx.decode("utf-8"),
                                          newdir_abs_path],
                                          capture_output=True)
                    if out.stdout == b"0":
                        logging.info(f"[uploader] file uploaded successfully and removed locally")
                    else:
                        logging.error(f"[uploader] uploading failed")
                        continue
                else:
                    logging.info("[uploader] FTP stop files uploading")
                    break
