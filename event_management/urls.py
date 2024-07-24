from django.urls import path

from . import views

urlpatterns = [
    path('calendar/', views.calendar_view, name='calendar'),
    path('get_events/', views.get_events, name='get_events'),
    path('add_event/', views.add_event, name='add_event'),
    path('update_event/<int:event_id>/', views.update_event, name='update_event'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
]
