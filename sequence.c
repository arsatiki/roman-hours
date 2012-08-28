#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <math.h>

#define EXACT_EPOCH (2451545.009)
#define EPOCH (2451545)
#define TAU (4*acos(0))
#define HOURS (12)

enum event_type {
	SUNRISE,
	SUNSET
};

typedef struct {
	time_t stamp;
	enum event_type type;
} event;

typedef long J2000_days;
typedef double julian;

const char* MESSAGES[24] = {
	"Sunrise. The first hour of day begins.\n",
	"The second hour of day begins.\n",
	"The third hour of day begins.\n",
	"The fourth hour of day begins.\n",
	"The fifth hour of day begins.\n",
	"The sixth hour of day begins.\n",
	"Noon. The seventh hour of day begins.\n",
	"The eight hour of day begins.\n",
	"The ninth hour of day begins.\n",
	"The tenth hour of day begins.\n",
	"The eleventh hour of day begins.\n",
	"The twelfth hour of day begins.\n",

	"Sunset. The first hour of night begins. First watch.\n",
	"The second hour of night begins.\n",
	"The third hour of night begins.\n",
	"The fourth hour of night begins. Second watch.\n",
	"The fifth hour of night begins.\n",
	"The sixth hour of night begins.\n",
	"Midnight. The seventh hour of night begins. Third watch.\n",
	"The eighth hour of night begins.\n",
	"The ninth hour of night begins.\n",
	"The tenth hour of night begins. Fourth watch.\n",
	"The eleventh hour of night begins.\n",
	"The twelfth hour of night begins.\n",
};


/* Fix. */
event make_event(time_t stamp, enum event_type type) {
	event e = {stamp, type};
	return e;
}

julian from_time_t(time_t t) {
	return ((double) t) / 86400.0 + 2440587.5;
}

time_t from_julian(julian jdn) {
	return (time_t)((jdn - 2440587.5) * 86400);
}

double dsin(double x) { return sin(TAU*x/360); }
double dcos(double x) { return cos(TAU*x/360); }
double arcsin(double x) { return 360 * asin(x) / TAU; }
double arccos(double x) { return 360 * acos(x) / TAU; }

void crossings(J2000_days t, double lat, double lon, event *rise, event *set) {
	julian noon, transit;
	noon = t + EXACT_EPOCH + lon / 360; 
	
	double M = fmod(357.5291 + 0.98560028 * (noon - 2451545), 360);
	double C = 1.9148 * dsin(M) + 0.0200 * dsin(2*M) + 0.0003 * dsin(3*M);
	double l = fmod(M + 102.9372 + C + 180, 360);
	
	transit = noon + 0.0053 * dsin(M) - 0.0069 * sin(2*l);
	
	double d = arcsin(dsin(l) * dsin(23.45));
	double num = dsin(-0.83) - dsin(lat) * dsin(d);
	double den = dcos(lat) * dcos(d);
	double w = arccos(num/den);

	*rise = make_event(from_julian(transit - w/360), SUNRISE);
	*set  = make_event(from_julian(transit + w/360), SUNSET);
}


int generate_events(double lat, double lon, time_t now, event** events) {
	int n = 20 * 365;
	int k;
	julian jnow;
	J2000_days t;
	event* evs;

	evs = (event*) calloc(2 * n, sizeof(event));	

	jnow = from_time_t(now);
	t = lround(jnow - EXACT_EPOCH - lon / 360);
		
	for (k = 0; k < n; k++) {
		crossings(t - 1 + k, lat, lon, &evs[2*k], &evs[2*k+1]);
	}
	
	*events = evs;
	return 2*n;
}


/********************** UI *********************/
int is_old(time_t stamp) {
	return difftime(time(NULL), stamp) > 60;
}


void sleep_until(time_t t) {
	double diff = difftime(t, time(NULL));
	if (diff > 0)
		sleep((time_t) diff);
}


void print_hours(event prev, event next) {
	int hour;
	double len = difftime(next.stamp, prev.stamp) / HOURS;
	time_t stamp;
	
	for (hour = 0; hour < HOURS; hour++) {
		stamp = prev.stamp + (time_t)(hour * len);
		if (is_old(stamp))
			continue;

		sleep_until(stamp);
		puts(MESSAGES[hour + prev.type * HOURS]);
		fflush(stdout);
	}
}


void print_events(event* events, int n_events) {
	int k = 1;
	event prev, next;

	for (k = 1; k < n_events; k++) {
		prev = events[k-1];
		next = events[k];
		if (difftime(next.stamp, time(NULL)) < 0)
			continue;
		print_hours(prev, next);
	}
}


int main(int argc, char** argv) {
	double lat, lon;
	event* events;
	int n_events;

	if (argc != 3) {
		printf("Usage: %s latitude longitude\n", argv[0]);
		exit(1);
	}
	lat = atof(argv[1]);
	lon = atof(argv[2]);
	
	n_events = generate_events(lat, lon, time(NULL), &events);
	print_events(events, n_events);
	printf("No more events.");
	
	return 0;
}