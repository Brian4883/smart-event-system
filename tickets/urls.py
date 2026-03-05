from django.urls import path
from . import views

urlpatterns = [

    path('purchase/<int:event_id>/', views.purchase_ticket, name='purchase_ticket'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),

]