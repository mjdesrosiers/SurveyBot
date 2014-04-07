import Adafruit_BBIO.UART as uart
from serial import Serial as ser
import time

#P9_13 => Serial4_Tx
#P9_11 => Serial4_Rx
uart.setup("UART4")
s = ser(port="/dev/ttyO2", baudrate=9600, timeout=1)
s.close()
s.open()

M1_OFFSET = 1
M2_OFFSET = 128

MIN_SIG = 0
MAX_SIG = 126

def make_msg(speed, motor_offset):
    return speed + motor_offset

while (True):
    for SIGNAL in range(MIN_SIG, MAX_SIG):
        msg1 = make_msg(SIGNAL, M1_OFFSET)
        msg2 = make_msg(SIGNAL, M2_OFFSET)
        s.write(chr(msg1))
        s.write(chr(msg2))
        print("writing value of '{}'".format(msg1))
        print("writing value of '{}'".format(msg2))
        time.sleep(0.2)
