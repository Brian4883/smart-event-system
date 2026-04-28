from django.urls import path
from .views import scan_ticket, my_tickets, purchase_ticket

urlpatterns = [

    path('purchase/<int:event_id>/', purchase_ticket, name='purchase_ticket'),
    path('my-tickets/', my_tickets, name='my_tickets'),
    path('scan/', scan_ticket, name='scan_ticket'),

]