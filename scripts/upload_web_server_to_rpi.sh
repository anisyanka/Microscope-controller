#!/bin/sh

local_sources_dir=`pwd`
local_sources_script_dir=$local_sources_dir/scripts
local_sources_web_dir=$local_sources_dir/web_server

source $local_sources_script_dir/rpi_ip.sh

rpi_web_dir=$rpi_src_path/web_server

# Create environment on RPI before copying
cd ..
ssh $ssh_arg $rpi_user@$rpi_ip "mkdir -p $rpi_web_dir; mkdir -p $rpi_web_dir/templates;" 
ssh $ssh_arg $rpi_user@$rpi_ip "mkdir -p $rpi_web_dir/static; mkdir -p $rpi_web_dir/static/css; mkdir -p $rpi_web_dir/static/images; mkdir -p $rpi_web_dir/static/scripts; mkdir -p $rpi_web_dir/stream_scripts; mkdir -p $rpi_web_dir/ftp_scripts;" 

# Send css
scp $scp_arg $local_sources_web_dir/static/css/styles.css \
        $rpi_user@$rpi_ip:$rpi_web_dir/static/css

# Send images
scp $scp_arg $local_sources_web_dir/static/images/favicon.ico \
        $rpi_user@$rpi_ip:$rpi_web_dir/static/images

# Send js scripts
scp $scp_arg $local_sources_web_dir/static/scripts/video_control.js \
    $local_sources_web_dir/static/scripts/buttons_control.js \
    $local_sources_web_dir/static/scripts/get_battery_level.js \
        $rpi_user@$rpi_ip:$rpi_web_dir/static/scripts

# Send stream scripts
scp $scp_arg $local_sources_web_dir/stream_scripts/camera_set_resolution_4k.sh \
    $local_sources_web_dir/stream_scripts/camera_set_resolution_1920x1080.sh \
    $local_sources_web_dir/stream_scripts/camera_capture_one_image_frame.sh \
    $local_sources_web_dir/stream_scripts/camera_capture_frames_continuously.sh \
        $rpi_user@$rpi_ip:$rpi_web_dir/stream_scripts

# Send FTP scripts
scp $scp_arg $local_sources_web_dir/ftp_scripts/check_conn.sh \
    $local_sources_web_dir/ftp_scripts/create_dir_on_server.sh \
    $local_sources_web_dir/ftp_scripts/does_file_exist_on_server_in_dir.sh \
    $local_sources_web_dir/ftp_scripts/does_file_exist_on_server.sh \
    $local_sources_web_dir/ftp_scripts/stop_ftp_transfer.sh \
    $local_sources_web_dir/ftp_scripts/upload_to_server.sh \
        $rpi_user@$rpi_ip:$rpi_web_dir/ftp_scripts

# Send Flask web-server
scp $scp_arg $local_sources_web_dir/templates/index.html \
    $local_sources_web_dir/templates/layout.html \
        $rpi_user@$rpi_ip:$rpi_web_dir/templates

scp $scp_arg $local_sources_web_dir/microscope_server.py \
    $local_sources_web_dir/helpers.py \
    $local_sources_web_dir/video_streamer.py \
    $local_sources_web_dir/config_reader.py \
    $local_sources_web_dir/ftp_uploader.py \
    $local_sources_web_dir/microscope_modbus.py \
    $local_sources_web_dir/microscope_server.service \
    $local_sources_web_dir/requirements.txt \
        $rpi_user@$rpi_ip:$rpi_web_dir/

# Send config
scp $scp_arg $local_sources_web_dir/microscope_server.conf \
        $rpi_user@$rpi_ip:$rpi_web_dir/

ssh $ssh_arg $rpi_user@$rpi_ip "chmod +x $rpi_web_dir/microscope_server.py"
