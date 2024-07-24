import json
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Event


@login_required(login_url="login")
def calendar_view(request):
    return render(request, 'event_management/calendar.html')


@login_required(login_url="login")
def get_events(request):
    events = Event.objects.all()
    event_list = []
    for event in events:
        event_list.append({
            'id': event.id,
            'title': event.title,
            'start': event.start_time.isoformat(),
            'end': event.end_time.isoformat(),
            'description': event.description
        })
    return JsonResponse(event_list, safe=False)


@login_required(login_url="login")
@csrf_exempt
def add_event(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        event = Event(
            title=data['title'],
            description=data.get('description', ''),
            start_time=datetime.fromisoformat(data['start']),
            end_time=datetime.fromisoformat(data['end']),
            owner=request.user
        )
        event.save()
        return JsonResponse({'status': 'success', 'id': event.id})
    return JsonResponse({'status': 'error'}, status=400)


@login_required(login_url="login")
@csrf_exempt
def update_event(request, event_id):
    if request.method == 'POST':
        event = Event.objects.get(id=event_id, owner=request.user)
        data = json.loads(request.body)
        event.title = data.get('title', event.title)
        event.description = data.get('description', event.description)
        event.start_time = datetime.fromisoformat(data['start'])
        event.end_time = datetime.fromisoformat(data['end'])
        event.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required(login_url="login")
@csrf_exempt
def delete_event(request, event_id):
    if request.method == 'POST':
        event = Event.objects.get(id=event_id, owner=request.user)
        event.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
