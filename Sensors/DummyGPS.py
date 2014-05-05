# -*- coding: utf-8 -*-
from Sensor import Sensor
import time
import Queue
from geopy import point
from geopy import distance
from Navigation import GPSPoint
import math as m


class DummyGPSSensor(Sensor):

    def __init__(self, master_queue, start_point, end_point, delay=0.5):
        super(DummyGPSSensor, self).__init__(master_queue, delay=delay)
        self.start_time = time.time()
        self.start_point = start_point
        self.end_point = end_point
        self.start_gps = GPSPoint.GPSPoint(pt=self.start_point)
        self.end_gps = GPSPoint.GPSPoint(pt=self.end_point)
        self.vincenty = distance.vincenty()
        self.speed = 10  # m / second
        self.brg = m.degrees(self.start_gps.bearing_to(self.end_gps))

    def data_source(self):
        t_delta = (time.time() + self.delay - self.start_time) / 1000.0
        x_delta = t_delta * self.speed
        point_now = self.vincenty.destination(self.start_point, self.brg, x_delta)
        x_from_start = self.vincenty.measure(point_now, self.start_point)
        dy = 0.01 * m.sin(x_from_start * 100)
        noise = dy
        mybrg = (self.brg + 90 + 360) % 360
        point_now = self.vincenty.destination(point_now, mybrg, noise)
        return (point_now.latitude, point_now.longitude, x_from_start)

    def cleanup(self):
        pass


if __name__ == "__main__":
    mq = Queue.Queue()
    lat_0, lon_0 = 38.035126, -78.496064
    start_pt = point.Point(lat_0, lon_0)
    end_pt = point.Point(lat_0 + 0.1, lon_0 - 0.1)
    gps = DummyGPSSensor(mq, start_pt, end_pt)

    dist = 1000.0  # meters

    endpt = gps.vincenty.destination(gps.start_point, gps.brg, dist)

    gps.start()  # lint:ok
    n_recv = 0
    vals = []
    while (n_recv < 200):
        if not mq.empty():
            n_recv += 1
            val = mq.get(block=True, timeout=0.5).data
            lat = val[0]
            lng = val[1]
            vals.append((lat, lng))
            #print(str(val) + ",")
    gps.stop()
    gps.thd.join()

    from Navigation import KMZ_Maker

    KMZ_Maker.make_kmz(vals)