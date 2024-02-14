#!/bin/sh
microscope_contoller_scr_dir=Microscope-controller
modbus_src_dir=$microscope_contoller_scr_dir/modbus_tcp_rtu_converter

rpi_user=pi
rpi_ip=192.168.1.55

# Create environment on RPI before copying
cd ..
ssh $rpi_user@$rpi_ip "cd ~;mkdir -p $modbus_src_dir; mkdir -p $modbus_src_dir/jsmn;" 

# Send sources
scp $modbus_src_dir/main.c \
    $modbus_src_dir/modbus_converter_config.c \
    $modbus_src_dir/modbus_converter_config.h \
    $modbus_src_dir/logger.c \
    $modbus_src_dir/logger.h \
    $modbus_src_dir/modbus_converter.conf \
    $modbus_src_dir/modbus_converter.service \
    $modbus_src_dir/camera_api.c \
    $modbus_src_dir/camera_api.h \
        $rpi_user@$rpi_ip:/home/pi/$modbus_src_dir

scp $modbus_src_dir/jsmn/jsmn.h \
        $rpi_user@$rpi_ip:/home/pi/$modbus_src_dir/jsmn

# Send Makefile
scp $microscope_contoller_scr_dir/Makefile \
        $rpi_user@$rpi_ip:/home/pi/$microscope_contoller_scr_dir
