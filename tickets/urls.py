from django.urls import path
from .views import scan_ticket, my_tickets, purchase_ticket

urlpatterns = [

    path('purchase/<int:event_id>/', views.purchase_ticket, name='purchase_ticket'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
    path('download/<int:ticket_id>/', views.download_ticket, name='download_ticket'),

]