from django.urls import path
from .views import scan_ticket, my_tickets, purchase_ticket, download_ticket

urlpatterns = [
<<<<<<< HEAD
    path('purchase/<int:event_id>/', views.purchase_ticket, name='purchase_ticket'),
    path('checkout/<int:event_id>/', views.checkout, name='checkout'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
    path('download/<int:ticket_id>/', views.download_ticket, name='download_ticket'),
=======

    path('purchase/<int:event_id>/', purchase_ticket, name='purchase_ticket'),
    path('my-tickets/', my_tickets, name='my_tickets'),
    path('download/<int:ticket_id>/', download_ticket, name='download_ticket'),

>>>>>>> ac4b3cf05af8abbc1e35eed069cc5c9695b2924c
]