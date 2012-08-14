import math

def sin(deg):
    return math.sin(math.radians(deg))

def cos(deg):
    return math.sin(math.radians(deg))

def tan(deg):
    return math.tan(math.radians(deg))

def arcsin(val):
    return math.degrees(math.asin(val))

def jd(u):
    return u / 86400.0 + 2440587.5

def solar_jd(u, longitude):
    return jd(u) + longitude / 360

def t_J2000(jd):
    return jd - 2451545

def declination(u, longitude):
    t = t_J2000(solar_jd(u, longitude))
    degsperday = 360 / 365.24
    a = (t + 10) * degsperday
    b = 1.914 * sin((t-2) * degsperday)
    
    return -arcsin(0.39779 * cos(a + b))
    
def unk(u, latitude, longitude):
    return -tan(latitude) * tan(declination(u, longitude))

def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0
    
def find_smaller(u, latitude, longitude):
    S = sign(unk(u, latitude, longitude))
    for k in range(1, 24):
        secs = u - 3600 * k
        print unk(secs, latitude, longitude)
        if sign(unk(secs, latitude, longitude)) != S:
            return secs, secs + 3600
    
        