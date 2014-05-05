import math as m
from geopy import point, distance
import TwoPointTrack
import KMZ_Maker
# http://williams.best.vwh.net/avform.htm#Crs

RADIUS_WGS84 = 6371  # km
LAX = (33.95, -118.4)
JFK = (40.63, -73.783)


class GPSPoint:

    def __init__(self, lat=None, lon=None, pt=None):
        if isinstance(pt, point.Point):
            self.pt = pt
            self.lat = pt.latitude
            self.lon = pt.longitude
        else:
            self.pt = None
            self.lat = lat
            self.lon = lon
        self.latr = m.radians(self.lat)
        self.lonr = m.radians(self.lon)

    def distance_to(self, other):
        """
        returns distance to other GPSPoint in km
        """
        lat1 = self.latr
        lon1 = -1 * self.lonr
        lat2 = other.latr
        lon2 = -1 * other.lonr

        arg = m.sqrt((m.sin((lat1 - lat2) / 2)) ** 2 +
                m.cos(lat1) * m.cos(lat2) * (m.sin((lon1 - lon2) / 2)) ** 2)
        arg_c = max(min(arg, 1.0), -1.0)
        if arg_c != arg:
            print("clamping arg from {} to {}".format(arg, arg_c))
        d = 2 * m.asin(arg_c)
        return d * RADIUS_WGS84

    def bearing_to(self, other):
        """
        return bearing to other GPSPoint, in radians.
        convert to degrees with math.degrees()
        """
        lat1 = self.latr
        lon1 = -1 * self.lonr
        lat2 = other.latr
        lon2 = -1 * other.lonr

        d = None
        try:
            tc1 = None
            d = m.acos(m.sin(lat1) * m.sin(lat2) + m.cos(lat1) * m.cos(lat2) * m.cos(lon1 - lon2))
            num = (m.sin(lat2) - m.sin(lat1) * m.cos(d))
            den = (m.sin(d) * m.cos(lat1))
            num_den = max(min(num / den, 1.0), -1.0)
            if (num / den != num_den):
                print("clamping num/den from {} to {}".format(num / den, num_den))
            if (m.sin(lon2 - lon1)) < 0:
                tc1 = m.acos(num_den)
            else:
                tc1 = 2 * m.pi - m.acos(num_den)

            return tc1
        except ValueError, ve:
            print(ve)
            num1 = m.sin(lat2)
            num2 = m.sin(lat1)
            num3 = m.cos(d)
            num = (m.sin(lat2) - m.sin(lat1) * m.cos(d))
            den1 = m.sin(d)
            den2 = m.cos(lat1)
            den = (m.sin(d) * m.cos(lat1))
            num_den = num / den
            print("num1={}\nnum2={}\nnum3={}\nnum={}\nden1={}\nden2={}\nden={}\nnum/den={}".format(
                num1, num2, num3, num, den1, den2, den, num_den))
            _num_den = max(min(num_den, 1.0), -1.0)
            print("old =>{}\nclamped=>{}".format(num_den, _num_den))
            tc = m.acos(_num_den)
            print("tc={}".format(tc))
            raise ve

    def project(self, bearing, dist):
        """
        Bearing in degrees.
        Distance in km.
        returns GPSPoint of projected loction
        """
        v = distance.vincenty()
        if (0 <= bearing <= 360):
            return GPSPoint(pt=v.destination(self.to_point(), bearing, dist))
        else:
            raise Exception("Bearing out of range: {}".format(bearing))

    def to_point(self):
        return point.Point(self.lat, self.lon)

    def __str__(self):
        return "<GPSPoint @ lat,lon={},{}>".format(self.lat, self.lon)

    def to_kmz_tup(self):
        return (self.lat, self.lon, 0)

x1 = GPSPoint(38.2551803588867,	-78.373649597168)
x2 = GPSPoint(38.2557323489097,	-78.373897494265)
x3 = GPSPoint(38.2554664611816,	-78.374397277832)
x4 = GPSPoint(38.2556619298459,	-78.3736972434101)
x5 = GPSPoint(38.2556190490723, -78.3738479614258)

Crossover1 = GPSPoint(38.2551803588867, -78.3736495971680)
Crossover2 = GPSPoint(38.2557323489097, -78.3738974942650)
Crossover3 = GPSPoint(38.2554664611816, -78.3743972778320)
Crossover4 = GPSPoint(38.2556619298459, -78.3738974942650)
Crossover5 = GPSPoint(38.2556619298459, -78.3736972434101)
CrossoverMid = GPSPoint(38.2556190490723, -78.3738479614258)

if __name__ == "__main__":
    straight_start = GPSPoint(38.255419, -78.373645)
    straight_end = GPSPoint(38.256626, -78.376774)
    straight_track = TwoPointTrack.TwoPointTrack(straight_start, straight_end)
    straight_track_distance = straight_track.track_distance
    straight_track_bearing = straight_track.brgd

    print("distance start to end is: {} km".format(straight_track_distance))
    print("bearing start to end is: {} deg".format(straight_track_bearing))

    SeamStartRearWP = GPSPoint(38.255647, -78.374364)
    inter_track_distance = straight_track.otd(SeamStartRearWP)
    print("distance from straight to seam is: {} km".format(inter_track_distance))

    inter_track_distance *= 1.5

    brg_x_track = straight_track_bearing - 90.0

    seam_start = straight_start.project(brg_x_track, -1 * inter_track_distance)

    line_start = straight_start.project(brg_x_track, -1 * inter_track_distance * 2)

    parts = [0.0, 0.25, 0.5, 0.75, 1.0]
    distances = [straight_track_distance * i for i in parts]
    straight_pts = [straight_start.project(straight_track_bearing, dist) for dist in distances]
    straight_tup = [pt.to_kmz_tup() for pt in straight_pts]
    seam_pts = [seam_start.project(straight_track_bearing, dist) for dist in distances]
    seam_tup = [pt.to_kmz_tup() for pt in seam_pts]
    line_pts = [line_start.project(straight_track_bearing, dist) for dist in distances]
    line_tup = [pt.to_kmz_tup() for pt in line_pts]
    all_pts = [(pt.lat, pt.lon, 0) for pt in straight_pts + seam_pts + line_pts]
    print(all_pts)
    KMZ_Maker.make_kmz(straight_tup, fname='Line0')
    KMZ_Maker.make_csv(straight_tup, fname='Line0')
    KMZ_Maker.make_kmz(seam_tup, fname='Line1')
    KMZ_Maker.make_csv(seam_tup, fname='Line1')
    KMZ_Maker.make_kmz(line_tup, fname='Line2')
    KMZ_Maker.make_csv(line_tup, fname='Line2')

    xover = [x1, x2, x3, x4, x5]
    xover_tup = [pt.to_kmz_tup() for pt in xover]
    KMZ_Maker.make_kmz(xover_tup, fname="xover")
    KMZ_Maker.make_csv(xover_tup, fname="xover")


