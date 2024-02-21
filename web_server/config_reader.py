import json

modbus_converter_conf="/home/pi/.microscope/modbus_converter.conf"
microscope_cmd_conf="/home/pi/.microscope/microscope_server.conf"

global mb_conv_data
global microscope_data

def read_all_configs():
    print("Read config files")
    with open(modbus_converter_conf, 'r') as j:
        global mb_conv_data
        mb_conv_data = json.loads(j.read())

    with open(microscope_cmd_conf, 'r') as m:
        global microscope_data
        microscope_data = json.loads(m.read())

    print()
    print("Modbus converter CONF:")
    print(mb_conv_data)
    print()

    print()
    print("Microscope server CONF:")
    print(microscope_data)
    print()

def get_modbus_tcp_rtu_converter_port():
    global mb_conv_data
    return int(mb_conv_data['modbus_port'])

def get_modbus_slave_id():
    global mb_conv_data
    return int(mb_conv_data['modbus_connected_microcontroller_slave_addr'])

def get_modbus_slave_timeout():
    global mb_conv_data
    return int(mb_conv_data['modbus_loss_connection_timeout_ms']) / 1000

def get_work_btn_focus_stepper_default_steps():
    global microscope_data
    return int(microscope_data['work_steps_cnt_focus_stepper'])

def get_work_btn_updown_stepper_default_steps():
    global microscope_data
    return int(microscope_data['work_steps_cnt_updown_stepper'])

def get_work_btn_leftright_stepper_default_steps():
    global microscope_data
    return int(microscope_data['work_steps_cnt_leftright_stepper'])

def get_swap():
    global microscope_data
    return microscope_data['swap_updown_and_leftright_logic']

def get_home_btn_focus_stepper_default_steps():
    global microscope_data
    return int(microscope_data['home_steps_cnt_focus_stepper'])

def get_home_btn_updown_stepper_default_steps():
    global microscope_data
    return int(microscope_data['home_steps_cnt_updown_stepper'])

def get_home_btn_leftright_stepper_default_steps():
    global microscope_data
    return int(microscope_data['home_steps_cnt_leftright_stepper'])

def get_repeat_cmd_perid_ms():
    global microscope_data
    return microscope_data['modbus_repeat_cmd_period_ms']

def get_soc_polling_period_ms():
    global microscope_data
    return microscope_data['modbus_soc_polling_period_ms']

def is_server_debug_enabled():
    global microscope_data
    return microscope_data['server_debug_mode']

def is_modbus_debug_enabled():
    global microscope_data
    return microscope_data['modbus_debug_mode']

def get_led_pwm_max_power():
    global microscope_data
    return int(microscope_data['modbus_led_max_pwm_percentage'])
