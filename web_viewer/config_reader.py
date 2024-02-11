import json

json_file_path="/home/pi/.modbus_converter/modbus_converter.conf"

def config_reader_retrieve_all_data():
    with open(json_file_path, 'r') as j:
        global contents
        contents = json.loads(j.read())

def config_reader_get_modbus_tcp_rtu_converter_port():
    return int(contents['modbus_port'])

def config_reader_get_modbus_slave_id():
    return int(contents['modbus_connected_microcontroller_slave_addr'])

def config_reader_get_modbus_slave_timeout():
    return int(contents['modbus_loss_connection_timeout_ms']) / 1000