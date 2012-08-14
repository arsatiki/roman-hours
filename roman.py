from datetime import datetime, time, timedelta
import sys
import time
import unix

HOURS = 'I II III IV V VI VII VIII IX X XI XII'.split()

def make(rise, sets, now=None):
    assert rise < sets
    if not now:
        now = time.time()

    day = 24*60*60
    
    if now < rise:
        return Night(sets - day, rise)
    if sets < now:
        return Night(sets, rise + day)
    return Day(rise, sets)

class Semi(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end
        
    def t(self, localtime):
        assert self.start < localtime < self.end
        full = self.end - self.start
        elapsed = localtime - self.start

        hour = 12.0 * elapsed / full
        hour_int = int(hour)
        minutes = (hour - hour_int) * 60
        return HOURS[hour_int], minutes

class Day(Semi):
    name = "Day"

class Night(Semi):
    name = "Night"

def main():
    start = 1344911607.0963488
    end = 1344968347.3134711

    semi = make(start, end)
    now = time.time()

    hour, minute = semi.t(now)
    
    print "%s hour of %s" % (hour, semi.name),
    if minute < 20:
        print "(early)"
    elif minute < 40:
        print "(halfway)"
    else:
        print "(late)"
        

if __name__ == '__main__':
    main()