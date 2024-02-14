import pymodbus.client as ModbusClient
from pymodbus import (
    ExceptionResponse,
    Framer,
    ModbusException,
    pymodbus_apply_logging_config,
)

from time import sleep

from helpers import helper_get_my_ip
import config_reader as conf_reader

def __set_bit(value, bit):
    return value | (1<<bit)

def __clear_bit(value, bit):
    return value & ~(1<<bit)

def modbus_connect_to_tcp_rtu_converter():
    ip = helper_get_my_ip()
    port = conf_reader.get_modbus_tcp_rtu_converter_port()
    global slave_addr
    slave_addr = conf_reader.get_modbus_slave_id()
    timeout = conf_reader.get_modbus_slave_timeout()

    print('Modbus TCP/RTU converter is running on {}:{}, slave addr={}, timeout={}s'.format(ip, port, slave_addr, timeout))

    # activate debugging
    # pymodbus_apply_logging_config("ERROR")

    global c
    c = ModbusClient.ModbusTcpClient(
                    host=ip,
                    port=port,
                    framer=Framer.SOCKET,
                    timeout=timeout)
        

def modbus_get_battery_level():
    c.connect()

    try:
        response = c.read_holding_registers(17, 1, slave=slave_addr)
    except ModbusException as exc:
        print(f"[ERR](Read battery level) --> Received ModbusException({exc}) from library")
        c.close()
        return 0

    if response.isError():
        print(f"[ERR](Read battery level) --> Received Modbus library error({response})")
        c.close()
        return 0
    if isinstance(response, ExceptionResponse):
        print(f"[ERR](Read battery level) --> Received Modbus library exception ({response})")
        # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
        c.close()

    c.close()
    return response.registers

def modbus_focus_motor_control(level):
    c.connect()

    if level == "upper":
        c.write_register(12, 1, slave=slave_addr)
    elif level == "lower":
        c.write_register(12, 32769, slave=slave_addr)

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
    swap = conf_reader.get_swap()

    # 2  - up\down addr
    # 4  - left\right
    # 12 - focus

    # Swap INdependent functions
    if position == "STOP":
        c.write_register(33, 1, slave=slave_addr)
    elif position == "HOME":
        focus_sign = conf_reader.focus_home_sign()
        updown_sign = conf_reader.updown_home_sign()
        leftright_sign = conf_reader.leftright_home_sign()

        if focus_sign == "+":
            c.write_register(12, 32767, slave=slave_addr)
        else:
            c.write_register(12, 65535, slave=slave_addr)
        sleep(0.05)

        if updown_sign == "+":
            c.write_register(2, 32767, slave=slave_addr)
        else:
            c.write_register(2, 65535, slave=slave_addr)
        sleep(0.05)

        if leftright_sign == "+":
            c.write_register(4, 32767, slave=slave_addr)
        else:
            c.write_register(4, 65535, slave=slave_addr)
    else:
        # Swap dependent functions
        if swap == "no":
            if position == "up":
                c.write_register(2, 1, slave=slave_addr)
            elif position == "down":
                c.write_register(2, 32769, slave=slave_addr)
            elif position == "right":
                c.write_register(4, 1, slave=slave_addr)
            elif position == "left":
                c.write_register(4, 32769, slave=slave_addr)
            elif position == "WORK":
                updown_def_steps = int(conf_reader.get_updown_stepper_default_steps())
                leftright_def_steps = int(conf_reader.get_leftright_stepper_default_steps())
                focus_def_steps = int(conf_reader.get_focus_stepper_default_steps())

                print("Up/down def steps cnt {}".format(updown_def_steps))
                print("Left/right def steps cnt {}".format(leftright_def_steps))
                print("focus_def_steps def steps cnt {}".format(focus_def_steps))

                if updown_def_steps < 0:
                    updown_def_steps = abs(updown_def_steps)
                    updown_def_steps = __set_bit(updown_def_steps, 15)

                if leftright_def_steps < 0:
                    leftright_def_steps = abs(leftright_def_steps)
                    leftright_def_steps = __set_bit(leftright_def_steps, 15)

                if focus_def_steps < 0:
                    focus_def_steps = abs(focus_def_steps)
                    focus_def_steps = __set_bit(focus_def_steps, 15)

                c.write_register(2, updown_def_steps, slave=slave_addr)
                sleep(0.05)
                c.write_register(4, leftright_def_steps, slave=slave_addr)
                sleep(0.05)
                c.write_register(12, focus_def_steps, slave=slave_addr)
            else:
                print("[ERR] Unknown command for motors")
        elif swap == "yes":
            if position == "up":
                c.write_register(4, 32769, slave=slave_addr)
            elif position == "down":
                c.write_register(4, 1, slave=slave_addr)
            elif position == "right":
                c.write_register(2, 32769, slave=slave_addr)
            elif position == "left":
                c.write_register(2, 1, slave=slave_addr)
            elif position == "WORK":
                updown_def_steps = int(conf_reader.get_updown_stepper_default_steps())
                leftright_def_steps = int(conf_reader.get_leftright_stepper_default_steps())
                focus_def_steps = int(conf_reader.get_focus_stepper_default_steps())

                print("Up/down def steps cnt {}".format(updown_def_steps))
                print("Left/right def steps cnt {}".format(leftright_def_steps))
                print("focus_def_steps def steps cnt {}".format(focus_def_steps))

                if updown_def_steps < 0:
                    updown_def_steps = abs(updown_def_steps)
                    updown_def_steps = __set_bit(updown_def_steps, 15)

                if leftright_def_steps < 0:
                    leftright_def_steps = abs(leftright_def_steps)
                    leftright_def_steps = __set_bit(leftright_def_steps, 15)

                if focus_def_steps < 0:
                    focus_def_steps = abs(focus_def_steps)
                    focus_def_steps = __set_bit(focus_def_steps, 15)

                c.write_register(4, updown_def_steps, slave=slave_addr)
                sleep(0.05)
                c.write_register(2, leftright_def_steps, slave=slave_addr)
                sleep(0.05)
                c.write_register(12, focus_def_steps, slave=slave_addr)
            else:
                print("[ERR] Unknown command for motors")
        else:
            print("[ERR] Unknown swap value in config file")

    sleep(0.05)
    c.close()
