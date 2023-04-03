# cal/views.py
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
import calendar
from django.urls import reverse_lazy, reverse
from calendarapp.check_salle import check_salle
from app.models import Formation,Salle
from calendarapp.models import Event, Event
from calendarapp.utils import Calendar
from calendarapp.forms import EventForm
from django.contrib import messages
from datetime import datetime, timedelta
from email.utils import parsedate_tz, mktime_tz

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


def remove(request):
    title = request.GET.get("title", None)
    event = Event.objects.get(title=title)
    event.formation.set_active(False)
    event.formation.save()
    if(event.formation.statut == "en cours"):
        event.formation.set_statut("non commencé")
        event.formation.save()
    event.delete()
    messages.success(request, 'Element supprimé avec succes')
    redirect_url = reverse('calendarapp:calendar')
    data = {'valid': 'success', 'message': 'Element supprimé avec succes', 'redirect_url': redirect_url}
    return JsonResponse(data)
    
def update(request):
    start_time = request.GET.get("start_time", None)
    end_time = request.GET.get("end_time", None)
    timestamp = mktime_tz(parsedate_tz(start_time))
    start = datetime(1970, 1, 1) + timedelta(seconds=timestamp)
    timestamp = mktime_tz(parsedate_tz(end_time))
    end = datetime(1970, 1, 1) + timedelta(seconds=timestamp)
    title = request.GET.get("title", None)
    event = Event.objects.get(title=title)
    event.start_time = start
    event.end_time = end
    event.title = title
    event.save()
    messages.success(request, 'Element edité avec succes')
    redirect_url = reverse('calendarapp:calendar')
    data = {'valid': 'success', 'message': 'Element edité avec succes', 'redirect_url': redirect_url}
    return JsonResponse(data)
    
    
class CalendarView(generic.ListView):
    model = Event
    template_name = "calendar.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        return context


def create_event(request):
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data["title"]
        formation = form.cleaned_data["formation"]
        salle = form.cleaned_data["salle"]
        start_time = form.cleaned_data["start_time"]
        end_time = form.cleaned_data["end_time"]
        Event.objects.get_or_create(
            title=title,
            formation=formation,
            salle=salle,
            start_time=start_time,
            end_time=end_time, 
            )
        return HttpResponseRedirect(reverse("calendarapp:calendar"))
    return render(request, "event.html", {"form": form})


class EventEdit(generic.UpdateView):
    model = Event
    fields = ["title", "formation", "salle", "start_time", "end_time"]
    template_name = "event.html"


def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    context = {"event": event, }
    return render(request, "event-details.html", context)


class CalendarViewNew(generic.View):
    template_name = "calendarapp/calendar.html"
    form_class = EventForm
    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        events = Event.objects.get_all_events()
        events_month = Event.objects.get_running_events()
        event_list = []
        for event in events:
            event_list.append(
                {
                    "title": event.title,
                    "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),

                }
            )
        context = {"form": forms, "events": event_list,
                   "events_month": events_month}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            salle = form.salle
            start_time = form.start_time 
            end_time = form.end_time
            if (check_salle(salle,start_time,end_time)==False):
                msg     = 'Session non crée ! veuillez réessayer.'
                success = False
                messages.error(request, msg)
                return redirect("calendarapp:calendar")
            else:
                form.save()
                msg     = 'Session crée avec succes.'
                success = True
                messages.success(request, msg)
                return redirect("calendarapp:calendar")
        context = {"form": forms,"msg" : msg, "success" : success}
        return render(request, self.template_name, context)

class DashboardView(View):
    template_name = "calendarapp/dashboard.html"

    def get(self, request, *args, **kwargs):
        events = Event.objects.get_all_events()
        running_events = Event.objects.get_running_events()
        latest_events = Event.objects.filter().order_by("-id")[:10]
        context = {
            "total_event": events.count(),
            "running_events": running_events,
            "latest_events": latest_events,
        }
        return render(request, self.template_name, context)
