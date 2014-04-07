# -*- coding: utf-8 -*-
from Sensors import DummyGPS
from Navigation import TwoPointTrack
from Navigation import GPSPoint
from Actuators import Steering_Drive_Actuator
from Actuators import Command_Packet
import Queue
import time

RUN_LENGTH = 30

def do_route_plan(track):
    gps_queue = Queue.Queue()
    sda_queue = Queue.Queue()
    st_pt = track.start.to_point()
    ed_pt = track.end.to_point()
    gps = DummyGPS.DummyGPSSensor(gps_queue, st_pt, ed_pt)
    sda = Steering_Drive_Actuator.Steering_Drive_Actuator(sda_queue, track)
    gps.start()
    sda.start()
    start = time.time()
    print("starting!")

    while ((time.time() - start) < 60):
        if not gps_queue.empty():
            pkt = gps_queue.get(block=True, timeout=0.5)
            data = pkt.data
            lat = data[0]
            lon = data[1]
            gps_now_pt = GPSPoint.GPSPoint(lat=lat, lon=lon)
            sda_queue.put(Command_Packet.Command_Packet("<__main__@Route_Planner>", {"gps_point": gps_now_pt}))
            if track.atd(gps_now_pt) > track.track_distance:
                print("reached end of track")
                break
    gps.stop()
    sda.stop()
    gps.thd.join()
    print("gps finished closing")
    sda.thd.join()
    print("sda finished closing")

    print("ran out of time, ending")

if __name__ == "__main__":
    lat_0, lon_0 = 38.035126, -78.496064
    lat_1, lon_1 = lat_0 + 0.003, lon_0 - 0.003
    start_gps = GPSPoint.GPSPoint(lat_0, lon_0)
    end_gps = GPSPoint.GPSPoint(lat_1, lon_1)
    print(start_gps)
    print(end_gps)
    track = TwoPointTrack.TwoPointTrack(start_gps, end_gps)
    do_route_plan(track)
