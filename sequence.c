#include <stdio.h>
#include <stdlib.h>
#include <time.h>

enum event_type {
	SUNRISE,
	SUNSET
};

typedef struct {
	time_t stamp;
	enum event_type type;
} event;

event make_event(time_t stamp, enum event_type type) {
	event e = {stamp, type};
	return e;
}

int generate_events(double lat, double lon, time_t now, event** events) {
	int n = 20 * 365;
	int k;
	(*events) = malloc(sizeof(event) * n);

	for (k = 0; k < n; k++)
		(*events)[k] = make_event(now + 60 * (k - 5), k % 2);

	return n;
}


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
	double hourlen = difftime(next.stamp, prev.stamp) / 12;
	char* type = (prev.type == SUNRISE)? "day": "night";
	time_t stamp;
	
	for (hour = 0; hour < 12; hour++) {
		stamp = prev.stamp + (time_t)(hour * hourlen);
		if (is_old(stamp))
			continue;

		sleep_until(stamp);
		printf("Hour %d (%s)\n", hour + 1, type); // Add more poesy.
		fflush(stdout);
	}
}

void print_events(event* events, int n_events) {
	int k = 1;
	/* I don't understand this code anymore */
	while (difftime(time(NULL), events[k].stamp) < 0)
		k++;
	
	for (; k < n_events; k++)
		print_hours(events[k-1], events[k]);
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