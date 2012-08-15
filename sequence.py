import sys
import time
import unix

from collections import namedtuple
from datetime import datetime


def times_for_cycle(latitude, longitude, now):
    Js = unix.JD_solar_noon(now, longitude)
    risesJD, setsJD = unix.times(Js, latitude, longitude)
    return unix.unix(risesJD), unix.unix(setsJD)


def cycle_J2000(longitude, now):
    return unix.current_cycle(now, longitude)


def generate_hours(start, end):
    diff = (end - start) / 12
    for k in range(12):
        yield start + k * diff, 'Hour %d starts' % (k + 1)


Event = namedtuple('Event', 'name time')


def generate_events(latitude, longitude, now, days=20 * 365):
    current_cycle = cycle_J2000(longitude, now)
    for offset in range(-1, days):
        cycle = current_cycle + offset

        rises, sets = times_for_cycle(latitude, longitude, cycle)
        yield Event('day', rises)
        yield Event('night', sets)


def is_old(stamp):
    return stamp < time.time() - 60


def sleep_until(stamp):
    time_left = stamp - time.time()
    if time_left > 0:
        time.sleep(time_left)
    else:
        print "Just a second..."
        time.sleep(1)  # A safety precaution.


def main():
    if len(sys.argv) != 3:
        print "Usage: %s latitude longitude" % sys.argv[0]
        sys.exit(1)

    lat, lon = map(float, sys.argv[1:])

    events = list(generate_events(lat, lon, time.time()))
    for k in range(len(events) - 1):
        prev, next = events[k], events[k + 1]
        if next.time < time.time():
            continue

        for stamp, text in generate_hours(prev.time, next.time):
            if is_old(stamp):
                continue

            sleep_until(stamp)
            print prev.name, text, str(datetime.now())


if __name__ == '__main__':
    main()
