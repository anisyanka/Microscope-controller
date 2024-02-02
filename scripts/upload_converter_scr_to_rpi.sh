modbus_src_dir=Modbus-TCP-RTU-Converter

rpi_user=pi
rpi_ip=192.168.1.55

# Create environment on RPI before copying
cd ..
ssh $rpi_user@$rpi_ip "cd ~;mkdir -p $modbus_src_dir; mkdir -p $modbus_src_dir/jsmn; mkdir -p $modbus_src_dir/scripts"

# Send sources
scp $modbus_src_dir/main.c \
    $modbus_src_dir/modbus_converter_config.c \
    $modbus_src_dir/modbus_converter_config.h \
    $modbus_src_dir/logger.c \
    $modbus_src_dir/logger.h \
    $modbus_src_dir/modbus_converter.conf \
    $modbus_src_dir/Makefile \
    $modbus_src_dir/modbus_converter.service \
    $modbus_src_dir/camera_api.c \
    $modbus_src_dir/camera_api.h \
        $rpi_user@$rpi_ip:/home/pi/$modbus_src_dir

scp $modbus_src_dir/jsmn/jsmn.h \
        $rpi_user@$rpi_ip:/home/pi/$modbus_src_dir/jsmn

# Send scripts for make install/uninstall targets
scp $modbus_src_dir/scripts/stop_modbus_converter_service_if_running.sh \
        $rpi_user@$rpi_ip:/home/pi/$modbus_src_dir/scripts
ssh $rpi_user@$rpi_ip "chmod +x $modbus_src_dir/scripts/stop_modbus_converter_service_if_running.sh"

# Send scripts to execute during runtime
scp $modbus_src_dir/scripts/update_host_ip_for_video_streaming.sh \
        $rpi_user@$rpi_ip:/home/pi/$modbus_src_dir/scripts
ssh $rpi_user@$rpi_ip "chmod +x $modbus_src_dir/scripts/update_host_ip_for_video_streaming.sh"

scp $modbus_src_dir/scripts/rpi_launch_udp_4k_soft_h264.sh \
        $rpi_user@$rpi_ip:/home/pi/$modbus_src_dir/scripts
ssh $rpi_user@$rpi_ip "chmod +x $modbus_src_dir/scripts/rpi_launch_udp_4k_soft_h264.sh"

scp $modbus_src_dir/scripts/rpi_launch_udp_1080p_mjpg.sh \
        $rpi_user@$rpi_ip:/home/pi/$modbus_src_dir/scripts
ssh $rpi_user@$rpi_ip "chmod +x $modbus_src_dir/scripts/rpi_launch_udp_1080p_mjpg.sh"

scp $modbus_src_dir/scripts/rpi_stop_video_stream.sh \
        $rpi_user@$rpi_ip:/home/pi/$modbus_src_dir/scripts
ssh $rpi_user@$rpi_ip "chmod +x $modbus_src_dir/scripts/rpi_stop_video_stream.sh"

scp $modbus_src_dir/scripts/linux_launch_udp_1080p_test_stream.sh \
        $rpi_user@$rpi_ip:/home/pi/$modbus_src_dir/scripts
ssh $rpi_user@$rpi_ip "chmod +x $modbus_src_dir/scripts/linux_launch_udp_1080p_test_stream.sh"

scp $modbus_src_dir/scripts/rpi_launch_tcp_1080p_mjpg.sh \
        $rpi_user@$rpi_ip:/home/pi/$modbus_src_dir/scripts
ssh $rpi_user@$rpi_ip "chmod +x $modbus_src_dir/scripts/rpi_launch_tcp_1080p_mjpg.sh"
