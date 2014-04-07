from Sensors import Acc_Gyro_Sensor
from Sensors import GPS_Sensor
import Queue

if __name__ == "__main__":
    print("starting!")
    sensor_data = Queue.Queue()
    data_out_queue = Queue.Queue()
    m = Acc_Gyro_Sensor.Magnetometer_Sensor(sensor_data)
    g = GPS_Sensor.GPS_Sensor(sensor_data, filter_tag="GPGGA")
    g.start()
    m.start()
    try:
        while True:
            if not sensor_data.empty():
                packet = sensor_data.get(block=True, timeout=0.5)
                if packet.originator == m:
                    print("received data point from magneto:\n\t{}".format(packet.data))
                elif packet.originator == g:
                    print("received data point from GPS:\n\t{}".format(packet.data))
                else:
                    print("received data from unknown:\n\t{}".format(packet.data))
    except KeyboardInterrupt:
        g.stop()
        m.stop()
        g.thd.join()
        m.thd.join()