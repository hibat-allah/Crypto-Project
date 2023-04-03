from datetime import datetime
from django.db import models
from django.urls import reverse
from django.db.models.fields.related import ForeignKey
from calendarapp.models import EventAbstract
from app.models import Formation,Salle
from datetime import datetime, timezone

class EventManager(models.Manager):
    """ Event manager """
    def set_formation(self):
        now = datetime.now(timezone.utc)
        events = Event.objects.all()
        for event in events:
            event.formation.set_active(True)
            event.formation.save()
            if(now>=event.end_time):
                event.formation.set_statut("terminé")
                event.formation.save()
            elif(event.start_time<=now):
                event.formation.set_statut("en cours")
                event.formation.save()
        return events
        
    def get_all_events(self):
        events = Event.objects.set_formation()
        events = Event.objects.all()
        return events

    def get_running_events(self):
        events = Event.objects.set_formation()
        running_events = Event.objects.filter(formation__statut='en cours').order_by("start_time")
        return running_events
    def get_upcoming_events(self):
        events = Event.objects.set_formation()
        upcoming_events = Event.objects.filter(formation__statut='non commencé').order_by("start_time")
        return upcoming_events
    def get_finished_events(self):
        events = Event.objects.set_formation()
        finished_events = Event.objects.filter(formation__statut='terminé').order_by("start_time")
        return finished_events




class Event(EventAbstract):
    """ Event model """

    title = models.CharField(max_length=200, unique=True)
    formation = models.ForeignKey("app.Formation", on_delete=models.CASCADE)
    salle = models.ForeignKey("app.Salle", on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    objects = EventManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("calendarapp:event-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("calendarapp:event-detail", args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
