modbus_src_dir=Modbus-TCP-RTU-Converter

rpi_user=pi
rpi_ip=192.168.1.55

# Create environment on RPI before copying
cd ..
ssh $rpi_user@$rpi_ip "cd ~;mkdir -p $modbus_src_dir; mkdir -p $modbus_src_dir/jsmn; mkdir -p $modbus_src_dir/scripts"

scp $modbus_src_dir/main.c \
    $modbus_src_dir/modbus_converter_config.c \
    $modbus_src_dir/modbus_converter_config.h \
    $modbus_src_dir/logger.c \
    $modbus_src_dir/logger.h \
    $modbus_src_dir/modbus_converter_config.json \
    $modbus_src_dir/Makefile \
    $modbus_src_dir/modbus_converter.service \
        $rpi_user@$rpi_ip:/home/pi/$modbus_src_dir

scp $modbus_src_dir/jsmn/jsmn.h \
        $rpi_user@$rpi_ip:/home/pi/$modbus_src_dir/jsmn

scp $modbus_src_dir/scripts/stop_modbus_converter_service_if_running.sh \
        $rpi_user@$rpi_ip:/home/pi/$modbus_src_dir/scripts
ssh $rpi_user@$rpi_ip "chmod +x $modbus_src_dir/scripts/stop_modbus_converter_service_if_running.sh"
