from django.urls import path
from .views import scan_ticket, my_tickets, purchase_ticket, download_ticket, checkout

urlpatterns = [
    path('purchase/<int:event_id>/', purchase_ticket, name='purchase_ticket'),
    path('checkout/<int:event_id>/', checkout, name='checkout'),
    path('my-tickets/', my_tickets, name='my_tickets'),
    path('download/<int:ticket_id>/', download_ticket, name='download_ticket'),
]