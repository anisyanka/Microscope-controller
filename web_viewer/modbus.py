from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

from helpers import helper_get_my_ip
from config_reader import config_reader_get_modbus_tcp_rtu_converter_port, config_reader_get_modbus_slave_id, config_reader_get_modbus_slave_timeout
from config_reader import config_reader_get_focus_stepper_default_steps, config_reader_get_updown_stepper_default_steps, config_reader_get_leftright_stepper_default_steps, config_reader_get_swap
from config_reader import config_reader_focus_home_sign, config_reader_updown_home_sign, config_reader_leftright_home_sign

def modbus_connect_to_tcp_rtu_converter():
    ip = helper_get_my_ip()
    port = config_reader_get_modbus_tcp_rtu_converter_port()
    global slave_addr
    slave_addr = config_reader_get_modbus_slave_id()
    timeout = config_reader_get_modbus_slave_timeout()

    print('Modbus TCP/RTU converter is running on {}:{}, slave addr={}, timeout={}s'.format(ip, port, slave_addr, timeout))

    global c
    c = ModbusTcpClient(host=ip, port=port, timeout=timeout)
        

def modbus_get_battery_level():
    c.connect()

    try:
        response = c.read_holding_registers(17, 1, slave=slave_addr)
    except ModbusException as exc:
        print(f"ERROR: exception in pymodbus {exc}")

    c.close()

    if response.isError():
        ret = 0
        print("[ERR] Read battery level failed")
    else:
        ret = response.registers

    return ret

def modbus_focus_motor_control(level):
    c.connect()

    if level == "upper":
        c.write_register(12, 1, slave=slave_addr)
    elif level == "lower":
        c.write_register(12, -1, slave=slave_addr)

    c.close()


def modbus_light_control(level):
    c.connect()

    if level == "upper":
        c.write_register(14, 1, slave=slave_addr)
    elif level == "lower":
        c.write_register(14, 0, slave=slave_addr)

    c.close()


def modbus_main_motors_control(position):
    c.connect()

    # Swap up and left AND right and down?
    swap = config_reader_get_swap()

    # 2  - up\down addr
    # 4  - left\right
    # 12 - focus

    if position == "up":
        if swap == "yes":
            c.write_register(4, -1, slave=slave_addr)
        else:
            c.write_register(2, 1, slave=slave_addr)

    elif position == "down":
        if swap == "yes":
            c.write_register(4, 1, slave=slave_addr)
        else:
            c.write_register(2, -1, slave=slave_addr)

    elif position == "left":
        if swap == "yes":
            c.write_register(2, -1, slave=slave_addr)
        else:
            c.write_register(4, -1, slave=slave_addr)

    elif position == "right":
        if swap == "yes":
            c.write_register(2, -1, slave=slave_addr)
        else:
            c.write_register(4, 1, slave=slave_addr)

    elif position == "WORK":
        updown_def_steps = int(config_reader_get_updown_stepper_default_steps())
        leftright_def_steps = int(config_reader_get_leftright_stepper_default_steps())
        focus_def_steps = int(config_reader_get_focus_stepper_default_steps())

        if swap == "yes":
            c.write_register(4, updown_def_steps, slave=slave_addr)
        else:
            c.write_register(2, updown_def_steps, slave=slave_addr)
    
        if swap == "yes":
            c.write_register(2, leftright_def_steps, slave=slave_addr)
        else:
            c.write_register(4, leftright_def_steps, slave=slave_addr)

        c.write_register(12, focus_def_steps, slave=slave_addr)

    elif position == "STOP":
        c.write_register(33, 1, slave=slave_addr)

    elif position == "HOME":
        focus_sign = config_reader_focus_home_sign()
        updown_sign = config_reader_updown_home_sign()
        leftright_sign = config_reader_leftright_home_sign()

        if focus_sign == "+":
            c.write_register(12, 32767, slave=slave_addr)
        else:
            c.write_register(12, -32767, slave=slave_addr)

        if updown_sign == "+":
            c.write_register(2, 32767, slave=slave_addr)
        else:
            c.write_register(2, -32767, slave=slave_addr)

        if leftright_sign == "+":
            c.write_register(4, 32767, slave=slave_addr)
        else:
            c.write_register(4, -32767, slave=slave_addr)
    else:
        print("[ERR] Wrong arg fr motors")

    c.close()
