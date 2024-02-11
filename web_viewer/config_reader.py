import json

modbus_converter_conf="/home/pi/.modbus_converter/modbus_converter.conf"
microscope_cmd_conf="/home/pi/.modbus_converter/web_viewer/microscope_cmd.conf"

def config_reader_retrieve_all_data():
    with open(modbus_converter_conf, 'r') as j:
        global mb_conv_data
        mb_conv_data = json.loads(j.read())

def config_reader_get_modbus_tcp_rtu_converter_port():
    return int(mb_conv_data['modbus_port'])

def config_reader_get_modbus_slave_id():
    return int(mb_conv_data['modbus_connected_microcontroller_slave_addr'])

def config_reader_get_modbus_slave_timeout():
    return int(mb_conv_data['modbus_loss_connection_timeout_ms']) / 1000

def config_reader_get_focus_stepper_default_steps():
    with open(microscope_cmd_conf, 'r') as m:
        microscope_data = json.loads(m.read())
    return int(microscope_data['work_steps_cnt_focus_stepper'])

def config_reader_get_updown_stepper_default_steps():
    with open(microscope_cmd_conf, 'r') as m:
        microscope_data = json.loads(m.read())
    return int(microscope_data['work_steps_cnt_updown_stepper'])

def config_reader_get_leftright_stepper_default_steps():
    with open(microscope_cmd_conf, 'r') as m:
        microscope_data = json.loads(m.read())
    return int(microscope_data['work_steps_cnt_leftright_stepper'])

def config_reader_get_swap():
    with open(microscope_cmd_conf, 'r') as m:
        microscope_data = json.loads(m.read())
    return microscope_data['swap_updown_and_lefnright_logic']

def config_reader_focus_home_sign():
    with open(microscope_cmd_conf, 'r') as m:
        microscope_data = json.loads(m.read())
    return microscope_data['home_btn_sign_focus_stepper']

def config_reader_updown_home_sign():
    with open(microscope_cmd_conf, 'r') as m:
        microscope_data = json.loads(m.read())
    return microscope_data['home_btn_sign_updown_stepper']

def config_reader_leftright_home_sign():
    with open(microscope_cmd_conf, 'r') as m:
        microscope_data = json.loads(m.read())
    return microscope_data['home_btn_sign_leftright_stepper']
