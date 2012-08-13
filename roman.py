from datetime import datetime, time, timedelta
import sys


HOURS = 'I II III IV V VI VII VIII IX X XI XII'.split()

def make(start, end, now=None):
    assert start < end
    if not now:
        now = datetime.now()

    rise = datetime.combine(datetime.today(), time(*start))
    sets = datetime.combine(datetime.today(), time(*end))
    day = timedelta(days=1)
    
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

        seconds = 12 * 3600 * elapsed.seconds / full.seconds
        hour, rem = divmod(seconds, 3600)
        return HOURS[hour], rem/60.

class Day(Semi):
    name = "Day"

class Night(Semi):
    name = "Night"

def main():
    start = (5, 31)
    end = (21, 18)

    semi = make(start, end)
    now = datetime.now()

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