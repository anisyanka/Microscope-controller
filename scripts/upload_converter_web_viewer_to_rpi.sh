#!/bin/sh
modbus_src_dir=Modbus-TCP-RTU-Converter

rpi_user=pi
rpi_ip=192.168.1.55

# Create environment on RPI before copying
cd ..
ssh $rpi_user@$rpi_ip "mkdir -p $modbus_src_dir/web_viewer; mkdir -p $modbus_src_dir/web_viewer/templates;" 
ssh $rpi_user@$rpi_ip "mkdir -p $modbus_src_dir/web_viewer/static; mkdir -p $modbus_src_dir/web_viewer/static/css; mkdir -p $modbus_src_dir/web_viewer/static/images; mkdir -p $modbus_src_dir/web_viewer/static/scripts; mkdir -p $modbus_src_dir/web_viewer/stream_scripts;" 

# Send css
scp $modbus_src_dir/web_viewer/static/css/styles.css \
        $rpi_user@$rpi_ip:/home/pi/$modbus_src_dir/web_viewer/static/css

# Send images
scp $modbus_src_dir/web_viewer/static/images/favicon.ico \
        $rpi_user@$rpi_ip:/home/pi/$modbus_src_dir/web_viewer/static/images

# Send js scripts
scp $modbus_src_dir/web_viewer/static/scripts/video_control.js \
    $modbus_src_dir/web_viewer/static/scripts/buttons_control.js \
    $modbus_src_dir/web_viewer/static/scripts/get_battery_level.js \
        $rpi_user@$rpi_ip:/home/pi/$modbus_src_dir/web_viewer/static/scripts

# Send stream scripts
scp $modbus_src_dir/web_viewer/stream_scripts/camera_set_resolution_4k.sh \
    $modbus_src_dir/web_viewer/stream_scripts/camera_set_resolution_1920x1080.sh \
    $modbus_src_dir/web_viewer/stream_scripts/webstream \
    $modbus_src_dir/web_viewer/stream_scripts/camera_stop_webstream_server.sh \
        $rpi_user@$rpi_ip:/home/pi/$modbus_src_dir/web_viewer/stream_scripts

# Send Flask web-server
scp $modbus_src_dir/web_viewer/templates/index.html \
    $modbus_src_dir/web_viewer/templates/layout.html \
        $rpi_user@$rpi_ip:/home/pi/$modbus_src_dir/web_viewer/templates
scp $modbus_src_dir/web_viewer/app.py \
    $modbus_src_dir/web_viewer/helpers.py \
    $modbus_src_dir/web_viewer/stream_control.py \
    $modbus_src_dir/web_viewer/config_reader.py \
    $modbus_src_dir/web_viewer/modbus.py \
    $modbus_src_dir/web_viewer/requirements.txt \
        $rpi_user@$rpi_ip:/home/pi/$modbus_src_dir/web_viewer/

# Send config
scp $modbus_src_dir/web_viewer/microscope_cmd.conf \
        $rpi_user@$rpi_ip:/home/pi/$modbus_src_dir/web_viewer/