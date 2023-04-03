import datetime
from calendarapp.models import Event


def check_salle(salle, start_time, end_time):
    events = Event.objects.filter(salle=salle)
    for event in events:
        if (start_time>=event.start_time and start_time<=event.end_time):
            return False
        if (end_time>=event.start_time and end_time<=event.end_time):
            return False
        if (event.start_time>=start_time and event.start_time<=end_time):
            return False
        if (event.end_time>=start_time and event.end_time<=end_time):
            return False
    return True
