# two point track
import math as m
import GPSPoint
from geopy import point, distance

LAX = (33.95, -118.4)
JFK = (40.63, -73.783)

MID = (34.5, -116.5)

CHO_1 = (38.041840, -78.494077)
CHO_2 = (38.040976, -78.495671)
CHO_3 = (38.041661, -78.494577)


class TwoPointTrack:

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.track_distance = self.start.distance_to(self.end)
        self.brg = self.start.bearing_to(self.end)
        self.brgd = m.degrees(self.brg)

    def otd(self, pt):
        dist_pt_rad = self.start.distance_to(pt) / GPSPoint.RADIUS_WGS84
        brg_pt = self.start.bearing_to(pt)
        #TODO range check argument to asin
        otd = m.asin(m.sin(dist_pt_rad) * m.sin(brg_pt - self.brg))
        return otd * GPSPoint.RADIUS_WGS84

    def atd(self, pt):
        dist_pt_rad = self.start.distance_to(pt) / GPSPoint.RADIUS_WGS84
        otd_rad = self.otd(pt) / GPSPoint.RADIUS_WGS84
        #TODO range check argument to asin
        atd = m.asin(m.sqrt((m.sin(dist_pt_rad)) ** 2 - (m.sin(otd_rad)) ** 2) / m.cos(otd_rad))
        return atd * GPSPoint.RADIUS_WGS84

    def __str__(self):
        return "TwoPointTrack: \n\tStart:{}\n\tStart:{}\n\tEnd:{}\n\tEnd:{}".format(
            self.start, self.startxy, self.end, self.endxy)

if __name__ == "__main__":
    g1 = GPSPoint.GPSPoint(LAX[0], LAX[1])
    g2 = GPSPoint.GPSPoint(JFK[0], JFK[1])
    g3 = GPSPoint.GPSPoint(MID[0], MID[1])
    tpt = TwoPointTrack(g1, g2)
    print("brg (dg)-> {}".format(tpt.brgd))
    print("otd (km)-> {}".format(tpt.otd(g3)))
    print("atd (km)-> {}".format(tpt.atd(g3)))

    lat_0, lon_0 = 38.035126, -78.496064
    start_pt = point.Point(lat_0, lon_0)
    end_pt = point.Point(lat_0 + 0.1, lon_0 - 0.1)
    st_gps = GPSPoint.GPSPoint(pt=start_pt)
    ed_gps = GPSPoint.GPSPoint(pt=end_pt)
    tpt = TwoPointTrack(st_gps, ed_gps)

    v = distance.vincenty()
    _10m_up = v.destination(start_pt, m.degrees(tpt.brg), .01)
    _10mgps = GPSPoint.GPSPoint(pt=_10m_up)
    print(st_gps)
    print(_10mgps)
    print(ed_gps)
    otd = tpt.otd(_10mgps)
    atd = tpt.atd(_10mgps)
    print("otd -> {}\natd -> {}".format(otd, atd))
    print("track bearing is: {}\nto point bearing is: {}".format(tpt.brg, tpt.start.bearing_to(_10mgps)))