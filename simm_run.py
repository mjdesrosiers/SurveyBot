# -*- coding: utf-8 -*-
#from Actuators import Motor_Controller
from Sensors import DummyGPS
from geopy import point
from Navigation import TwoPointTrack
from Navigation import GPSPoint
import Queue
import time

if __name__ == "__main__":
    data_queue = Queue.Queue()
    cmd_queue = Queue.Queue()

    lat_0, lon_0 = 38.035126, -78.496064
    start_pt = point.Point(lat_0, lon_0)
    end_pt = point.Point(lat_0 + 0.1, lon_0 - 0.1)
    gps = DummyGPS.DummyGPSSensor(data_queue, start_pt, end_pt)

    start_gps = GPSPoint.GPSPoint(pt=start_pt)
    end_gps = GPSPoint.GPSPoint(pt=end_pt)

    track = TwoPointTrack.TwoPointTrack(start_gps, end_gps)

 #   mc = Motor_Controller.Motor_Controller()
    gps.start()
  #  mc.start()
    start = time.time()
    print("starting!")

    while ((time.time() - start) < 30):
        if not data_queue.empty():
            pkt = data_queue.get(block=True, timeout=0.5)
            data = pkt.data
            lat = data[0]
            lon = data[1]
            #print("lat, lon = <{},{}>".format(lat, lon))
            now_pt = GPSPoint.GPSPoint(lat=lat, lon=lon)
            otd = track.otd(now_pt)
            atd = track.atd(now_pt)
            print("otd,{},atd,{}".format(otd, atd))

    print("ran out of time, ending")