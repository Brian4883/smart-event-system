from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket
from events.models import Event
import uuid


def purchase_ticket(request, event_id):

    event = get_object_or_404(Event, id=event_id)

    ticket_code = str(uuid.uuid4())

    ticket = Ticket.objects.create(
        user=request.user,
        event=event,
        ticket_code=ticket_code
    )

    return redirect('my_tickets')


def my_tickets(request):

    tickets = Ticket.objects.filter(user=request.user)

    return render(request, 'my_tickets.html', {'tickets': tickets})