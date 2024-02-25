import os
import socket

HOST_IP_CONFIG="/home/pi/.microscope/host_ip.conf"

def get_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_str = s.getsockname()[0]
    s.close()
    return ip_str

def update_host_ip_config(host_ip):
    f = open(HOST_IP_CONFIG, "w")
    f.write(host_ip + '\n')
    f.close()
