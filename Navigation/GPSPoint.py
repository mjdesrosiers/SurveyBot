import math as m
from geopy import point
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
            num_den= num/den
            print("num1={}\nnum2={}\nnum3={}\nnum={}\nden1={}\nden2={}\nden={}\nnum/den={}".format(
                num1, num2, num3, num, den1, den2, den, num_den))
            _num_den = max(min(num_den, 1.0), -1.0)
            print("old =>{}\nclamped=>{}".format(num_den, _num_den))
            tc = m.acos(_num_den)
            print("tc={}".format(tc))
            raise ve

    def to_point(self):
        return point.Point(self.lat, self.lon)

    def __str__(self):
        return "<GPSPoint @ lat,lon={},{}>".format(self.lat, self.lon)


if __name__ == "__main__":
    pt1 = point.Point(LAX[0], LAX[1])
    pt2 = point.Point(JFK[0], JFK[1])
    g1 = GPSPoint(LAX[0], LAX[1])
    g1 = GPSPoint(pt=pt1)
    g2 = GPSPoint(JFK[0], JFK[1])
    g2 = GPSPoint(pt=pt2)
    print(m.degrees(g1.bearing_to(g2)))
    print(g1.distance_to(g2))
