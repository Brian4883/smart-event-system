from django.shortcuts import render, redirect
from .models import Event
from .forms import EventForm


def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})


def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()

    return render(request, 'events/create_event.html', {'form': form})