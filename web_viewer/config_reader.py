import json

modbus_converter_conf="/home/pi/.modbus_converter/modbus_converter.conf"
microscope_cmd_conf="/home/pi/.modbus_converter/web_viewer/microscope_cmd.conf"

def get_modbus_tcp_rtu_converter_port():
    with open(modbus_converter_conf, 'r') as j:
        mb_conv_data = json.loads(j.read())
    return int(mb_conv_data['modbus_port'])

def get_modbus_slave_id():
    with open(modbus_converter_conf, 'r') as j:
        mb_conv_data = json.loads(j.read())
    return int(mb_conv_data['modbus_connected_microcontroller_slave_addr'])

def get_modbus_slave_timeout():
    with open(modbus_converter_conf, 'r') as j:
        mb_conv_data = json.loads(j.read())
    return int(mb_conv_data['modbus_loss_connection_timeout_ms']) / 1000

def get_focus_stepper_default_steps():
    with open(microscope_cmd_conf, 'r') as m:
        microscope_data = json.loads(m.read())
    return int(microscope_data['work_steps_cnt_focus_stepper'])

def get_updown_stepper_default_steps():
    with open(microscope_cmd_conf, 'r') as m:
        microscope_data = json.loads(m.read())
    return int(microscope_data['work_steps_cnt_updown_stepper'])

def get_leftright_stepper_default_steps():
    with open(microscope_cmd_conf, 'r') as m:
        microscope_data = json.loads(m.read())
    return int(microscope_data['work_steps_cnt_leftright_stepper'])

def get_swap():
    with open(microscope_cmd_conf, 'r') as m:
        microscope_data = json.loads(m.read())
    return microscope_data['swap_updown_and_leftright_logic']

def focus_home_sign():
    with open(microscope_cmd_conf, 'r') as m:
        microscope_data = json.loads(m.read())
    return microscope_data['home_btn_sign_focus_stepper']

def updown_home_sign():
    with open(microscope_cmd_conf, 'r') as m:
        microscope_data = json.loads(m.read())
    return microscope_data['home_btn_sign_updown_stepper']

def leftright_home_sign():
    with open(microscope_cmd_conf, 'r') as m:
        microscope_data = json.loads(m.read())
    return microscope_data['home_btn_sign_leftright_stepper']

def get_repeat_cmd_perid_ms():
    with open(microscope_cmd_conf, 'r') as m:
        microscope_data = json.loads(m.read())
    return microscope_data['modbus_repeat_cmd_period_ms']

def get_soc_polling_period_ms():
    with open(microscope_cmd_conf, 'r') as m:
        microscope_data = json.loads(m.read())
    return microscope_data['modbus_soc_polling_period_ms']
