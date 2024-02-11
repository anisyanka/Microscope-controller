from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

from helpers import helper_get_my_ip
from config_reader import config_reader_get_modbus_tcp_rtu_converter_port, config_reader_get_modbus_slave_id, config_reader_get_modbus_slave_timeout

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
    response = c.read_input_registers(17, 1, slave=slave_addr)
    c.close()

    print(response.registers)
    return response.registers

def modbus_focus_motor_control(level):
    c.connect()

    # if level == "upper":
    #     c.write_register()
    # elif level == "lower":
    #     c.write_register()

    c.close()
    print()


def modbus_light_control(level):
    c.connect()

    # if level == "upper":
    #     c.write_register()
    # elif level == "lower":
    #     c.write_register()

    c.close()
    print()


def modbus_main_motors_control(position):
    c.connect()

    # if position == "up":
    #     c.write_register()
    # elif position == "down":
    #     c.write_register()
    # elif position == "left":
    #     c.write_register()
    # elif position == "right":
    #     c.write_register()
    # elif position == "WORK":
    #     c.write_register()
    # elif position == "STOP":
    #     c.write_register()
    # elif position == "HOME":
    #     c.write_register()

    c.close()
    print()