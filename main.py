
# LAT =  60.194025
LONG = 24.941135
EPOCH = 2451545.0009

def JDN(year, month, day):
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    
    return day + (153*m + 2) // 5 + 365*y + y//4 - y//100 + y//400 - 32045
    
def Jdate(year, month, day, hour, minute, second, microseconds=0):
    JD = JDN(year, month, day)
    JD += float(hour - 12) / 24
    JD += float(minute / 1440)
    JD += float(second / 86400)
    JD += float(microseconds / 1000000)
    return JD

def main():
    n = round(J_date - EPOCH - LONG / 360.0)
    J = EPOCH + n + LONG / 360.0
    pass

if __name__ == '__main__':
    main()