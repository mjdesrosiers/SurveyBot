# -*- coding: utf-8 -*-
from Actuator import Actuator

SIMM_MODE_ACTIVE = False
try:
    import Adafruit_BBIO.UART as uart
except Exception:
    SIMM_MODE_ACTIVE = True
    print("Adafruit's IO Library not installed")
    print("Setting SIMM mode to Active!")
import serial
from Command_Packet import Command_Packet
import Queue
import time
from pprint import pprint as pp

M0_OFFSET = 63
M1_OFFSET = 191
FULL_FWD = 63
FULL_REV = -63

CHANNEL_0 = "ch0"
CHANNEL_1 = "ch1"

CHNS_DICT = {CHANNEL_0: M0_OFFSET, CHANNEL_1: M1_OFFSET}



class Motor_Controller(Actuator):

    def __init__(self, master_queue, get_timeout=0.05, UART_PORT=2):
        super(Motor_Controller, self).__init__(master_queue, get_timeout=get_timeout)
        self.UART_PORT_str = "UART" + str(UART_PORT)
        self.SERIAL_PORT_str = "/dev/ttyO" + str(UART_PORT)
        self.ser = None
        self.speeds = {CHANNEL_0:0, CHANNEL_1:0}
        if not SIMM_MODE_ACTIVE:
            self.initialize_UART(uart_port_str=self.UART_PORT_str, ser_port_str=self.SERIAL_PORT_str)

    def initialize_UART(self, uart_port_str, ser_port_str):
        print("Initializing motor controller UART")
        try:
            uart.setup(uart_port_str)
            self.ser = serial.Serial(port=ser_port_str, baudrate=9600, timeout=1)
            self.ser.close()
            self.ser.open()
            print("Successfully initialized UART")
        except Exception as e:
            print("error in opening uart.")
            print(e)

    def act_on_cmd(self, cmd):
        if not isinstance(cmd, Command_Packet):
            print("Command was not a Command_Packet. Not acting on it.")
            return
        if SIMM_MODE_ACTIVE:
            pp(cmd.command)
        if CHANNEL_0 in cmd.command:
            try:
                self.send_serial_cmd(self.build_serial_cmd(CHANNEL_0, cmd.command[CHANNEL_0]))
            except ValueError as ve:
                print(ve)
        if CHANNEL_1 in cmd.command:
            try:
                self.send_serial_cmd(self.build_serial_cmd(CHANNEL_1, cmd.command[CHANNEL_1]))
            except ValueError as ve:
                print(ve)

    def build_serial_cmd(self, channel, value):
        if abs(value) <= 63:
            offset = CHNS_DICT[channel]
            out = chr(value + offset)
            self.speeds[channel] = value
            return out
        else:
            raise ValueError("Commmand out of value range: channel:{}, value:{}".format(channel, value))

    def send_serial_cmd(self, value):
        if not SIMM_MODE_ACTIVE:
            self.ser.write(value)

    def cleanup(self):
        try:
            print("cleaning up " + str(self))
            print("stopping channel 0")
            self.send_serial_cmd(self.build_serial_cmd(CHANNEL_0, 0))
            print("stopping channel 1")
            self.send_serial_cmd(self.build_serial_cmd(CHANNEL_1, 1))
            if not SIMM_MODE_ACTIVE:
                self.ser.close()
        except Exception, e:
            print("error in closing {}: {}".format(self, e))
        print("motor controller finished closing successfully")

    def __str__(self):
        return "Motor_Controller actuator on UART=<{}>, Port=<{}>".format(self.UART_PORT_str, self.SERIAL_PORT_str)

    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    q = Queue.Queue()
    mc = Motor_Controller(q)
    print(mc)
    mc.start()
    times = 0
    early_end = False
    try:
        while times < 10:
            if (times % 2 == 0):
                q.put(Command_Packet("<__main__>", {"ch0": 50, "ch1": 0}))
            else:
                q.put(Command_Packet("<__main__>", {"ch0": 0, "ch1": 50}))
            time.sleep(3)
            times = times + 1
    except KeyboardInterrupt:
        print("caught keyboardinterrupt")
        mc.stop()
        mc.thd.join()
        early_end = True
    if not early_end:
        mc.stop()
        mc.thd.join()


