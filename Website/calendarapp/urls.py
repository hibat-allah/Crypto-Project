from django.urls import path, include, re_path
from . import views
from .views.other_views import DashboardView
from .views.event_list import AllEventsListView,RunningEventsListView,UpcomingEventsListView,FinishedEventsListView
from .views import remove,update
app_name = "calendarapp"


urlpatterns = [
    path("calender", views.CalendarViewNew.as_view(), name="calendar"),
    path("event/new/", views.create_event, name="event_new"),
    path("event/edit/<int:pk>/", views.EventEdit.as_view(), name="event_edit"),
    path("event/<int:event_id>/details/", views.event_details, name="event-detail"),
    path(
        "all-event-list/",
        AllEventsListView.as_view(),
        name="all_events",
    ),
    path(
        "running-event-list/",
        RunningEventsListView.as_view(),
        name="running_events",
    ),
    path(
        "upcoming-event-list/",
        UpcomingEventsListView.as_view(),
        name="upcoming_events",
    ),
    path(
        "finished-event-list/",
        FinishedEventsListView.as_view(),
        name="finished_events",
    ),
    path("dashboardcalendar/", DashboardView.as_view(), name="dashboardcalendar"),
    re_path(r'^remove', remove, name='remove'),
    re_path(r'^update', update, name='update'),
    path('', include('app.urls')),
    
]

