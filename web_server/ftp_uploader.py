import subprocess
import logging
from time import sleep
import threading
import config_reader as conf_reader


class FtpUploader:
    # FTP current state
    is_ftp_enabled = 0


    def __init__(self):
        self.is_ftp_enabled = 0


    def enable_ftp_transferring(self):
        self.is_ftp_enabled = 1
        logging.info("FTP enabled")


    def disable_ftp_transferring(self):
        self.is_ftp_enabled = 0
        logging.info("FTP disabled")


    def is_ftp_transferring_enabled(self):
        return self.is_ftp_enabled
