#!/bin/sh
modbus_src_dir=Modbus-TCP-RTU-Converter

rpi_user=pi
rpi_ip=192.168.1.55

# Create environment on RPI before copying
cd ..
ssh $rpi_user@$rpi_ip "mkdir -p $modbus_src_dir/web_viewer; mkdir -p $modbus_src_dir/web_viewer/templates;" 
ssh $rpi_user@$rpi_ip "mkdir -p $modbus_src_dir/web_viewer/static; mkdir -p $modbus_src_dir/web_viewer/static/css; mkdir -p $modbus_src_dir/web_viewer/static/images; mkdir -p $modbus_src_dir/web_viewer/static/scripts;" 

# Send css
scp $modbus_src_dir/web_viewer/static/css/styles.css \
        $rpi_user@$rpi_ip:/home/pi/$modbus_src_dir/web_viewer/static/css

# Send images
scp $modbus_src_dir/web_viewer/static/images/favicon.ico \
        $rpi_user@$rpi_ip:/home/pi/$modbus_src_dir/web_viewer/static/images

# Send scripts
scp $modbus_src_dir/web_viewer/static/scripts/video_control.js \
    $modbus_src_dir/web_viewer/static/scripts/focus_control.js \
    $modbus_src_dir/web_viewer/static/scripts/get_battery_level.js \
        $rpi_user@$rpi_ip:/home/pi/$modbus_src_dir/web_viewer/static/scripts

# Send Flask web-server
scp $modbus_src_dir/web_viewer/templates/index.html \
    $modbus_src_dir/web_viewer/templates/layout.html \
        $rpi_user@$rpi_ip:/home/pi/$modbus_src_dir/web_viewer/templates
scp $modbus_src_dir/web_viewer/app.py \
    $modbus_src_dir/web_viewer/helpers.py \
    $modbus_src_dir/web_viewer/stream_control.py \
    $modbus_src_dir/web_viewer/requirements.txt \
        $rpi_user@$rpi_ip:/home/pi/$modbus_src_dir/web_viewer/
