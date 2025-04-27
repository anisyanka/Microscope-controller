#!/bin/sh

local_sources_dir=`pwd`
local_sources_script_dir=$local_sources_dir/scripts
local_sources_modbus_dir=$local_sources_dir/modbus_tcp_rtu_converter

source $local_sources_script_dir/rpi_ip.sh

rpi_modbus_src_dir=$rpi_src_path/modbus_tcp_rtu_converter

# Create environment on RPI before copying
cd ..
ssh $rpi_user@$rpi_ip "cd ~;mkdir -p $rpi_modbus_src_dir; mkdir -p $rpi_modbus_src_dir/jsmn;" 

# Send sources
scp $local_sources_modbus_dir/main.c \
    $local_sources_modbus_dir/modbus_converter_config.c \
    $local_sources_modbus_dir/modbus_converter_config.h \
    $local_sources_modbus_dir/logger.c \
    $local_sources_modbus_dir/logger.h \
    $local_sources_modbus_dir/modbus_converter.conf \
    $local_sources_modbus_dir/modbus_converter.service \
    $local_sources_modbus_dir/camera_api.c \
    $local_sources_modbus_dir/camera_api.h \
        $rpi_user@$rpi_ip:$rpi_modbus_src_dir

scp $local_sources_modbus_dir/jsmn/jsmn.h \
        $rpi_user@$rpi_ip:$rpi_modbus_src_dir/jsmn

# Send Makefile
scp $local_sources_dir/Makefile \
        $rpi_user@$rpi_ip:$rpi_src_path
