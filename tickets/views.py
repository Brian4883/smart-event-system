import io
import uuid

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from .models import Ticket
from events.models import Event


def build_ticket_pdf(ticket):
    buffer = io.BytesIO()
    width, height = letter
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle(f"Ticket-{ticket.ticket_code}")

    pdf.setFont('Helvetica-Bold', 22)
    pdf.drawString(40, height - 60, 'EventSphere Ticket')

    pdf.setFont('Helvetica-Bold', 16)
    pdf.drawString(40, height - 100, ticket.event.title)

    pdf.setFont('Helvetica', 12)
    attendee_name = ticket.user.get_full_name() or ticket.user.username
    pdf.drawString(40, height - 130, f'Attendee: {attendee_name}')
    pdf.drawString(40, height - 150, f'Ticket Code: {ticket.ticket_code}')
    pdf.drawString(40, height - 170, f'Date: {ticket.event.start_date}')
    if ticket.event.end_date:
        pdf.drawString(40, height - 190, f'Ends: {ticket.event.end_date}')
    pdf.drawString(40, height - 210, f'Location: {ticket.event.location}')

    price_text = 'Free' if ticket.event.price == 0 else f'Ksh {ticket.event.price}'
    pdf.drawString(40, height - 230, f'Price: {price_text}')
    if ticket.event.price_details:
        pdf.drawString(40, height - 250, f'Note: {ticket.event.price_details}')

    pdf.setFont('Helvetica-Bold', 14)
    pdf.drawString(40, height - 285, 'Scan this QR at entry:')

    if ticket.qr_code:
        try:
            pdf.drawImage(ticket.qr_code.path, width - 200, height - 330, width=140, height=140)
        except Exception:
            pass

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer


def email_ticket_attachments(request, user, tickets):
    if not user.email or not tickets:
        return False

    event_title = tickets[0].event.title
    subject = f'Your EventSphere Ticket(s) for {event_title}'
    body = (
        f'Hello {user.get_full_name() or user.username},\n\n'
        f'Your free ticket(s) for "{event_title}" have been generated. Please find the attached PDF ticket(s) below.\n\n'
        'If you do not receive this email, check your spam folder or contact support.\n\n'
        'Thank you for using EventSphere.'
    )

    email = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email])
    for ticket in tickets:
        pdf = build_ticket_pdf(ticket)
        email.attach(f'ticket_{ticket.ticket_code}.pdf', pdf.getvalue(), 'application/pdf')

    try:
        email.send(fail_silently=False)
        return True
    except Exception as exc:
        messages.warning(request, f'Unable to send ticket email: {exc}')
        return False


@login_required
def purchase_ticket(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    qty = request.GET.get('qty', '1')
    try:
        qty = int(qty)
    except ValueError:
        qty = 1
    qty = max(1, min(qty, 10))

    created_tickets = []
    for _ in range(qty):
        ticket_code = str(uuid.uuid4())
        ticket = Ticket.objects.create(
            user=request.user,
            event=event,
            ticket_code=ticket_code
        )
        created_tickets.append(ticket)

    if event.price == 0:
        emailed = email_ticket_attachments(request, request.user, created_tickets)
        if emailed:
            messages.success(request, 'Free ticket(s) generated and emailed to you. You can also download them from My Tickets.')
        else:
            messages.warning(request, 'Your free ticket(s) were generated, but email delivery failed. Please download them from My Tickets.')
    else:
        messages.success(request, 'Ticket purchase complete. You can download your ticket(s) from My Tickets.')

    return redirect('my_tickets')


@login_required
def download_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    buffer = build_ticket_pdf(ticket)
    return FileResponse(buffer, as_attachment=True, filename=f'ticket_{ticket.ticket_code}.pdf')


@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'tickets/my_tickets.html', {'tickets': tickets})