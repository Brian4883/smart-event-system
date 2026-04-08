from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import EventForm


def event_list(request):
    events = Event.objects.filter(is_approved=True)  # only approved events
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, event_id):
    event = Event.objects.get(id=event_id, is_approved=True)
    return render(request, 'events/event_detail.html', {'event': event})


@login_required
def create_event(request):
    if request.user.role == "organizer" and not request.user.is_verified:
        messages.error(request, "Your account is not verified yet.")
        return redirect("organizer_dashboard")

    if request.method == 'POST':
        form = EventForm(request.POST)

        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user

            event.is_approved = False

            event.save()

            messages.info(request, "Event submitted for approval.")
            return redirect('organizer_dashboard')

    else:
        form = EventForm()

    return render(request, 'events/create_event.html', {'form': form})

@login_required
def edit_event(request, event_id):
    event = Event.objects.get(id=event_id, organizer=request.user)

    form = EventForm(request.POST or None, request.FILES or None, instance=event)

    if form.is_valid():
        form.save()
        messages.success(request, "Event updated successfully")
        return redirect("organizer_dashboard")

    return render(request, "events/create_event.html", {"form": form})

@login_required
def delete_event(request, event_id):
    event = Event.objects.get(id=event_id, organizer=request.user)
    event.delete()
    messages.success(request, "Event deleted")
    return redirect("organizer_dashboard")