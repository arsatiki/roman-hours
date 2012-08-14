import sys
import time
import unix

from datetime import datetime

def times(latitude, longitude, now):
    Js = unix.solar_noon(now, longitude)
    risesJD, setsJD = unix.times(Js, latitude, longitude)
    return unix.unix(risesJD), unix.unix(setsJD)

def adjust(rises, sets, now):
    day = 24 * 60 * 60
    if now < rises:
        return sets - day, rises, 'night'
    if now > sets:
        return sets, rises + day, 'night'
    return rises, sets, 'day'

def generate_events(start, end):
    diff = (end - start) / 12
    for k in range(12):
        yield start + k * diff, 'Hour %d starts' % (k + 1)

def is_old(stamp):
    return stamp < time.time() - 60

def sleep_until(stamp):
    time_left = stamp - time.time() 
    if time_left > 0:
        time.sleep(time_left)

def main():
    if len(sys.argv) != 3:
        print "Usage: %s latitude longitude" % sys.argv[0]
        sys.exit(1)
    
    lat, lon = map(float, sys.argv[1:])
    
    while True:
        now = time.time()
        rises, sets = times(lat, lon, now)
        start, end, cycle = adjust(rises, sets, now)

        for stamp, text in generate_events(start, end):
            if is_old(stamp):
                continue
            
            sleep_until(stamp)
            print cycle, text, str(datetime.now())


if __name__ == '__main__':
    main()