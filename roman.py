from datetime import datetime, time, timedelta
import sys

HOURS = 'I II III IV V VI VII VIII IX X XI XII'.split()

def main():
    start = (5, 29)
    end = (23, 21)

    rise = datetime.combine(datetime.today(), time(*start))
    sets = datetime.combine(datetime.today(), time(*end))
    now = datetime.now()
    diff = sets - rise

    if rise < now < sets:
        scale = 12 * 3600 * (now - rise).seconds / diff.seconds
        print "Current time: ", timedelta(seconds=scale)
        

    print "Sunrise at %d:%d" % start
    for k in range(12):
        hour_starts = rise + k * diff // 12
        hour_ends = rise + (k + 1) * diff // 12
        print HOURS[k],
        if hour_starts < now < hour_ends:
            print '**',

        print "\t ends at %02d:%02d" % (hour_ends.hour, hour_ends.minute)
        

if __name__ == '__main__':
    main()