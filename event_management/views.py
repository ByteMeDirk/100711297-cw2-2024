from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .forms import EventForm
from .models import Event

@login_required(login_url="login")
def calendar(request):
    events = Event.objects.all()
    return render(request, 'event_management/calendar.html', {'events': events})


@login_required(login_url="login")
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)  # Save the form temporarily without committing to the database
            event.owner = request.user  # Set the owner of the event to the current user
            event.save()  # Now save the event to the database
            return redirect('calendar')
    else:
        form = EventForm()
    return render(request, 'event_management/add_event.html', {'form': form})


@login_required(login_url="login")
def list_events(request):
    """List users created events"""
    events = Event.objects.filter(owner=request.user)
    return render(request, 'event_management/list_events.html', {'events': events})


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
        })
    return JsonResponse(event_list, safe=False)


@login_required(login_url="login")
def edit_event(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('calendar')
    else:
        form = EventForm(instance=event)
    return render(request, 'event_management/edit_event.html', {'form': form, 'event': event})


@login_required(login_url="login")
def delete_event(request, event_id):
    event = Event.objects.get(id=event_id)
    event.delete()
    return redirect('calendar')
