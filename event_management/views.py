import json
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Event


@login_required(login_url="login")
def calendar_view(request):
    """
    This view renders the calendar page.
    """
    return render(request, "event_management/calendar.html")


@login_required(login_url="login")
def get_events(request):
    """
    This view returns a list of events in JSON format.
    """
    events = Event.objects.all()
    event_list = []
    for event in events:
        event_list.append(
            {
                "id": event.id,
                "title": event.title,
                "start": event.start_time.isoformat(),
                "end": event.end_time.isoformat(),
                "description": event.description,
                "editable": event.owner == request.user,
            }
        )
    return JsonResponse(event_list, safe=False)


@login_required(login_url="login")
@csrf_exempt
def add_event(request):
    """
    This view adds a new event to the calendar.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        start_time = datetime.fromisoformat(data["start"])
        end_time = datetime.fromisoformat(data["end"])

        # Round to nearest 15 minutes
        start_time = start_time.replace(
            minute=(start_time.minute // 15) * 15, second=0, microsecond=0
        )
        end_time = end_time.replace(
            minute=(end_time.minute // 15) * 15, second=0, microsecond=0
        )

        event = Event(
            title=data["title"],
            description=data.get("description", ""),
            start_time=start_time,
            end_time=end_time,
            owner=request.user,
        )
        event.save()
        messages.success(request, "Event added successfully.")
        return JsonResponse({"status": "success", "id": event.id})
    messages.error(request, "Failed to add event.")
    return JsonResponse({"status": "error"}, status=400)


@login_required(login_url="login")
@csrf_exempt
def update_event(request, event_id):
    """
    This view updates an existing event in the calendar.
    """
    if request.method == "POST":
        try:
            event = Event.objects.get(id=event_id, owner=request.user)
        except Event.DoesNotExist:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Event not found or you do not have permission",
                },
                status=404,
            )

        data = json.loads(request.body)
        start_time = datetime.fromisoformat(data["start"])
        end_time = datetime.fromisoformat(data["end"])

        # Round to nearest 15 minutes
        start_time = start_time.replace(
            minute=(start_time.minute // 15) * 15, second=0, microsecond=0
        )
        end_time = end_time.replace(
            minute=(end_time.minute // 15) * 15, second=0, microsecond=0
        )

        event.title = data.get("title", event.title)
        event.description = data.get("description", event.description)
        event.start_time = start_time
        event.end_time = end_time
        event.save()
        messages.success(request, "Event updated successfully.")
        return JsonResponse({"status": "success"})
    messages.error(request, "Failed to update event.")
    return JsonResponse({"status": "error"}, status=400)


@login_required(login_url="login")
@csrf_exempt
def delete_event(request, event_id):
    """
    This view deletes an existing event from the calendar.
    """
    if request.method == "POST":
        try:
            event = Event.objects.get(id=event_id, owner=request.user)
        except Event.DoesNotExist:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Event not found or you do not have permission",
                },
                status=404,
            )

        event.delete()
        messages.success(request, "Event deleted successfully.")
        return JsonResponse({"status": "success"})
    messages.error(request, "Failed to delete event.")
    return JsonResponse({"status": "error"}, status=400)
