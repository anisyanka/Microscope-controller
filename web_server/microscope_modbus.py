import pymodbus.client as ModbusClient
from pymodbus import (
    ExceptionResponse,
    Framer,
    ModbusException,
    pymodbus_apply_logging_config,
)
from pymodbus.framer.socket_framer import ModbusSocketFramer

from time import sleep
import helpers as helper
import config_reader as conf_reader

class ModbusMicroscope:
    def __init__(self):
        self.cur_pwm_duty = 0
        self.last_bat_level = 0
        self.debug = False

        self.ip = helper.get_my_ip()
        self.port = conf_reader.get_modbus_tcp_rtu_converter_port()
        self.timeout = conf_reader.get_modbus_slave_timeout()
        self.slave_addr = conf_reader.get_modbus_slave_id()
        print('Modbus TCP/RTU converter is running on {}:{}, stm32 slave addr={}, timeout={}s'.format(self.ip, self.port, self.slave_addr, self.timeout))

        # connect to Modbus TCP/RTU converter
        self.clinet = ModbusClient.ModbusTcpClient(
                            host=self.ip,
                            port=self.port,
                            framer=ModbusSocketFramer,
                            timeout=self.timeout)
        self.clinet.connect()
        assert self.clinet.connected
        if self.clinet.connected == True:
            print('Connected to Modbus TCP/RTU client OK')
        else:
            print('Connected to Modbus TCP/RTU client FAILED')

    def debug_mode(self, debug):
        # activate debugging
        if debug == True:
            self.debug = True
            pymodbus_apply_logging_config("DEBUG")
        else:
            self.debug = False

    def get_bat_level(self):
        try:
            response = self.clinet.read_holding_registers(17, 1, slave=self.slave_addr)
        except ModbusException as exc:
            print(f"[ERR](Read battery level) --> Received ModbusException({exc}) from library")
            return self.last_bat_level

        if response.isError():
            print(f"[ERR](Read battery level) --> Received Modbus library error({response})")
            return self.last_bat_level
        elif isinstance(response, ExceptionResponse): # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
            print(f"[ERR](Read battery level) --> Received Modbus library exception ({response})")
            return self.last_bat_level
        else:
            self.last_bat_level = int(response.registers[0])

        print('BAT level = {}%'.format(self.last_bat_level))
        return self.last_bat_level

    def focus_motor_control(self, level):
        if level == "upper":
            self.clinet.write_register(12, 1, slave=self.slave_addr)
        elif level == "lower":
            self.clinet.write_register(12, 65535, slave=self.slave_addr)
        else:
            print("[ERR] wrong cmd")

    def light_control(self, level):
        MAX_PWM_DUTY = conf_reader.get_led_pwm_max_power()

        if level == "upper":
            self.cur_pwm_duty += 1
            if self.cur_pwm_duty > MAX_PWM_DUTY:
                self.cur_pwm_duty = MAX_PWM_DUTY
            self.clinet.write_register(14, self.cur_pwm_duty, slave=self.slave_addr)
        elif level == "lower":
            if self.cur_pwm_duty > 0:
                self.cur_pwm_duty -= 1
            self.clinet.write_register(14, self.cur_pwm_duty, slave=self.slave_addr)
        else:
            print("[ERR] wrong cmd")
        
        print("Light PWM=%d%% %s\n" % (self.cur_pwm_duty, "(MAX)" if self.cur_pwm_duty >= MAX_PWM_DUTY else ""))

    def main_motors_control(self, position):
        # Swap up and left AND right and down?
        swap = conf_reader.get_swap()

        # 2  - up\down addr
        # 4  - left\right
        # 12 - focus

        # Swap INdependent functions
        if position == "STOP":
            self.clinet.write_register(33, 1, slave=self.slave_addr)
        else:
            # Swap dependent functions
            if swap == "no":
                if position == "up":
                    self.clinet.write_register(2, 1, slave=self.slave_addr)
                elif position == "down":
                    self.clinet.write_register(2, 65535, slave=self.slave_addr)
                elif position == "right":
                    self.clinet.write_register(4, 1, slave=self.slave_addr)
                elif position == "left":
                    self.clinet.write_register(4, 65535, slave=self.slave_addr)
                elif position == "HOME" or position == "WORK":
                    if position == "WORK":
                        updown_steps = conf_reader.get_work_btn_updown_stepper_default_steps()
                        leftright_steps = conf_reader.get_work_btn_leftright_stepper_default_steps()
                        focus_steps = conf_reader.get_work_btn_focus_stepper_default_steps()
                    elif position == "HOME":
                        updown_steps = conf_reader.get_home_btn_updown_stepper_default_steps()
                        leftright_steps = conf_reader.get_home_btn_leftright_stepper_default_steps()
                        focus_steps = conf_reader.get_home_btn_focus_stepper_default_steps()

                    if updown_steps != 0:
                        if updown_steps < 0:
                            updown_steps &= 0xffff
                        self.clinet.write_register(2, updown_steps, slave=self.slave_addr)
                        sleep(0.01)

                    if leftright_steps != 0:
                        if leftright_steps < 0:
                            leftright_steps &= 0xffff
                        self.clinet.write_register(4, leftright_steps, slave=self.slave_addr)
                        sleep(0.01)

                    if focus_steps != 0:
                        if focus_steps < 0:
                            focus_steps &= 0xffff
                        self.clinet.write_register(12, focus_steps, slave=self.slave_addr)
                else:
                    print("[ERR] Unknown command for motors")
            elif swap == "yes":
                if position == "up":
                    self.clinet.write_register(4, 65535, slave=self.slave_addr)
                elif position == "down":
                    self.clinet.write_register(4, 1, slave=self.slave_addr)
                elif position == "right":
                    self.clinet.write_register(2, 65535, slave=self.slave_addr)
                elif position == "left":
                    self.clinet.write_register(2, 1, slave=self.slave_addr)
                elif position == "HOME" or position == "WORK":
                    if position == "WORK":
                        updown_steps = conf_reader.get_work_btn_updown_stepper_default_steps()
                        leftright_steps = conf_reader.get_work_btn_leftright_stepper_default_steps()
                        focus_steps = conf_reader.get_work_btn_focus_stepper_default_steps()
                    elif position == "HOME":
                        updown_steps = conf_reader.get_home_btn_updown_stepper_default_steps()
                        leftright_steps = conf_reader.get_home_btn_leftright_stepper_default_steps()
                        focus_steps = conf_reader.get_home_btn_focus_stepper_default_steps()

                    if updown_steps != 0:
                        if updown_steps < 0:
                            updown_steps &= 0xffff
                        self.clinet.write_register(4, updown_steps, slave=self.slave_addr)
                        sleep(0.01)

                    if leftright_steps != 0:
                        if leftright_steps < 0:
                            leftright_steps &= 0xffff
                        self.clinet.write_register(2, leftright_steps, slave=self.slave_addr)
                        sleep(0.01)

                    if focus_steps != 0:
                        if focus_steps < 0:
                            focus_steps &= 0xffff
                        self.clinet.write_register(12, focus_steps, slave=self.slave_addr)
                else:
                    print("[ERR] Unknown command for motors")
            else:
                print("[ERR] Unknown swap value in config file")

        sleep(0.01)
