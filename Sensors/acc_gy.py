import smbus
from Sensor import Sensor
import math
import Queue

# i2c2, SCL => P9_19
# i2c2, SDA => P9_20

# i2c address of device
ADDR = 0x1D

# addresses of acceleration components
# these do not seem to work
OUT_X_L_A = 0x28
OUT_X_H_A = 0x29
OUT_Y_L_A = 0x2A
OUT_Y_H_A = 0x2B
OUT_Z_L_A = 0x2C
OUT_Z_H_A = 0x2D

# addresses of magnetometer components
# these actually seem to work
OUT_X_L_M = 0x08
OUT_X_H_M = 0x09
OUT_Y_L_M = 0x0A
OUT_Y_H_M = 0x0B
OUT_Z_L_M = 0x0C
OUT_Z_H_M = 0x0D

# addresses of control registers

ACC_MAG_CTRL0 = 0x1F
ACC_MAG_CTRL1 = 0x20
ACC_MAG_CTRL2 = 0x21
ACC_MAG_CTRL3 = 0x22
ACC_MAG_CTRL4 = 0x23
ACC_MAG_CTRL5 = 0x24
ACC_MAG_CTRL6 = 0x25
ACC_MAG_CTRL7 = 0x26

#[0:3] => update rate
#[5:7] => xyz enable

#0101 => 50 Hz update

ACC_MAG_ACC_ENABLE = 0b10010111
ACC_MAG_MAG_ENABLE = 0b10000000


class Magnetometer_Sensor(Sensor):

    def __init__(self, master_queue, delay=0.1):
        super(Magnetometer_Sensor, self).__init__(master_queue, delay=delay)
        self.bus = smbus.SMBus(1)
        self.I2C_ADDR = ADDR
        self.init_sensor()

    def init_sensor(self):
        # turn on magnetometer
        # need to write to CTRL7
        self.bus.write_byte_data(self.I2C_ADDR, ACC_MAG_CTRL5, 0x64)
        self.bus.write_byte_data(self.I2C_ADDR, ACC_MAG_CTRL6, 0x20)
        self.bus.write_byte_data(self.I2C_ADDR, ACC_MAG_CTRL7, ACC_MAG_MAG_ENABLE)

        # turn on accelerometer
        # need to write to CTRL1
        self.bus.write_byte_data(self.I2C_ADDR, ACC_MAG_CTRL2, 0x00)
        self.bus.write_byte_data(self.I2C_ADDR, ACC_MAG_CTRL1, ACC_MAG_ACC_ENABLE)

    def get_16_bit(self, addr, reg_lo, reg_hi):
        lo = self.bus.read_byte_data(addr, reg_lo)
        hi = self.bus.read_byte_data(addr, reg_hi)
        val = ((hi << 8) | lo)
        if (val > 32768):
            val = val - 2 ** 16
        return val

    def compute_heading(self, x, y, z):
        add = 0
        if (y > 0):
            add = 90
        elif (y < 0):
            add = 270
        elif (y == 0) and (x < 0):
            return 180
        elif (y == 0) and (x > 0):
            return 0

        return add - math.atan2(x, y) * 180 / math.pi

    def data_source(self):
        mag_x = self.get_16_bit(self.I2C_ADDR, OUT_X_L_M, OUT_X_H_M)
        mag_y = self.get_16_bit(self.I2C_ADDR, OUT_Y_L_M, OUT_Y_H_M)
        mag_z = self.get_16_bit(self.I2C_ADDR, OUT_Z_L_M, OUT_Z_H_M)
        return self.compute_heading(mag_x, mag_y, mag_z)


    def cleanup(self):
        pass

    def __str__(self):
        return "<I2C magnetometer sensor @ {}>".format(self.I2C_ADDR)

    def __repr__(self):
        return self.__str__()



if __name__ == "__main__":
    print("starting!")
    sensor_data = Queue.Queue()
    m = Magnetometer_Sensor(sensor_data)
    m.start()
    while True:
        if not sensor_data.empty():
            packet = sensor_data.get(block=True, timeout=0.5)
            if packet.originator == m:
                print("received data point from GPS:\n\t{}".format(packet.data))
            else:
                print("received data from unknown:\n\t{}".format(packet.data))
