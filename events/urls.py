from django.urls import path
from .views import edit_event, event_list, event_detail, create_event, delete_event

urlpatterns = [
    path('events/', event_list, name='event_list'),
    path('events/create/', create_event, name='create_event'),
    path('events/<int:event_id>/', event_detail, name='event_detail'),
    path('events/edit/<int:event_id>/', edit_event, name='edit_event'),
    path('events/delete/<int:event_id>/', delete_event, name='delete_event'),

]