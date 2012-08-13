from datetime import datetime
import math
import time

LON_scaled = -24.9375 / 360
EPOCH = 2451545.0009
LAT = 60.1708

def degsin(x):
    return math.sin(math.radians(x))

def degcos(x):
    return math.cos(math.radians(x))

def jd(u):
    return u / 86400.0 + 2440587.5

def unix(JDN):
    return (JDN - 2440587.5) * 86400

def current_cycle():
    return round(jd(time.time()) - EPOCH - LON_scaled)

def solar_noon():
    return EPOCH + current_cycle() + LON_scaled

def localtime(jd):
    return datetime.fromtimestamp(unix(jd))

def M(Jstar): # g
    return (357.5291 + 0.98560028 * (Jstar - 2451545)) % 360

def ec_long(m):
    c1 = 1.9148 * degsin(m)
    c2 = 0.0200 * degsin(2 * m)
    c3 = 0.0003 * degsin(3 * m)
    
    return (m + 102.9372 + c1+c2+c3 + 180) % 360

def times(Jstar, latitude):
    m = M(Jstar)
    lamb = ec_long(m)
    
    transit = Jstar + 0.0053 * degsin(m) - 0.0069 * degsin(2 * lamb)
    declination = decl(lamb)

    angle = math.degrees(hourangle(latitude, declination))
    return transit - angle/360, transit + angle/360

def decl(lamb):
    return math.degrees(math.asin(degsin(lamb) * degsin(23.45)))

def hourangle(latitude, declination):
    num = degsin(-0.83) - degsin(latitude) * degsin(declination)
    den = degcos(latitude) * degcos(declination)

    if num/den < 0:
        print "It's night"

    return math.acos(num/den)