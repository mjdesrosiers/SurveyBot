import Adafruit_BBIO.UART as uart
from serial import Serial as ser
from Sensor import Sensor
import Queue


class GPS_Sensor(Sensor):

    def __init__(self, master_queue, delay=0, filter_tag=None):
        super(GPS_Sensor, self).__init__(master_queue, delay=delay)
        self.filter_tag = filter_tag
        self.init_uart()

    def init_uart(self):
        uart.setup("UART4")
        self.port = ser(port="/dev/ttyO4", baudrate=57600, timeout=1)

    def data_source(self):
        return self.get_line(start_filter=self.filter_tag)

    def parse_GPGGA(self, sentence):
        splits = sentence.split(",")
        title = splits[0]
        time = splits[1]
        lat = splits[2]
        lat_dir = splits[3]
        lng = splits[4]
        lng_dir = splits[5]

        if lat:
            latf = float(lat)
            lat_int = int(latf / 100)
            lat_min = latf - lat_int * 100
            lat_dec = lat_min / 60
            lat_number = lat_int + lat_dec

        if lng:
            lngf = float(lng)
            lng_int = int(lngf / 100)
            lng_min = lngf - lng_int * 100
            lng_dec = lng_min / 60
            lng_number = lng_int + lng_dec

        return title + " @ " + time + " : " + str(lat_number) + lat_dir + ", " + str(lng_number) + lng_dir

    def get_line(self, start_filter=None):
        out = self.port.readline()[:-1]
        if (start_filter is None):
            return out
        else:
            if (out.startswith("$" + start_filter)):
                if start_filter == "GPGGA":
                    return self.parse_GPGGA(out)
                return out

    def cleanup(self):
        print("Calling cleanup on " + str(self))
        if self.port.isOpen():
            self.port.close()

    def __str__(self):
        return "<GPS Sensor on {}>".format(self.port.port)

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    print("starting!")
    sensor_data = Queue.Queue()
    g = GPS_Sensor(sensor_data, filter_tag = "GPGGA")
    g.start()
    while True:
        if not sensor_data.empty():
            packet = sensor_data.get(block=True, timeout=0.5)
            if packet.originator == g:
                print("received data point from GPS:\n\t{}".format(packet.data))
            else:
                print("received data from unknown:\n\t{}".format(packet.data))

