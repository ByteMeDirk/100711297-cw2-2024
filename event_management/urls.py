from django.urls import path

from .views import calendar, add_event, get_events, list_events, edit_event, delete_event

urlpatterns = [
    path("calendar/", calendar, name="calendar"),
    path("add_event/", add_event, name="add_event"),
    path("get_events/", get_events, name="get_events"),
    path("list_events/", list_events, name="list_events"),
    path("edit_event/<int:event_id>/", edit_event, name="edit_event"),
    path("delete_event/<int:event_id>/", delete_event, name="delete_event"),
]
