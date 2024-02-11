import json

modbus_converter_conf="/home/pi/.modbus_converter/modbus_converter.conf"
microscope_cmd_conf="/home/pi/.modbus_converter/web_viewer/microscope_cmd.conf"

def config_reader_retrieve_all_data():
    with open(modbus_converter_conf, 'r') as j:
        global mb_conv_data
        mb_conv_data = json.loads(j.read())

    with open(microscope_cmd_conf, 'r') as m:
        global microscope_data
        microscope_data = json.loads(m.read())

def config_reader_get_modbus_tcp_rtu_converter_port():
    return int(mb_conv_data['modbus_port'])

def config_reader_get_modbus_slave_id():
    return int(mb_conv_data['modbus_connected_microcontroller_slave_addr'])

def config_reader_get_modbus_slave_timeout():
    return int(mb_conv_data['modbus_loss_connection_timeout_ms']) / 1000
