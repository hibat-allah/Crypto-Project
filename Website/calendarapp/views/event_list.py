from django.views.generic import ListView

from calendarapp.models import Event


class AllEventsListView(ListView):
    """ All event list views """

    template_name = "calendarapp/all_events_list.html"
    model = Event

    def get_queryset(self):
        return Event.objects.get_all_events()


class RunningEventsListView(ListView):
    """ Running events list view """

    template_name = "calendarapp/running_events_list.html"
    model = Event

    def get_queryset(self):
        return Event.objects.get_running_events()
        
class UpcomingEventsListView(ListView):
    """ Running events list view """

    template_name = "calendarapp/upcoming_events_list.html"
    model = Event

    def get_queryset(self):
        return Event.objects.get_upcoming_events()
        
class FinishedEventsListView(ListView):
    """ Running events list view """

    template_name = "calendarapp/finished_events_list.html"
    model = Event

    def get_queryset(self):
        return Event.objects.get_finished_events()
