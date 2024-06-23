from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.list_events, name='list_events'),
    path('<int:event_id>/', views.detail_event, name='detail_event'),
    path('create/', views.create_event, name='create_event'),
    path('<int:event_id>/update/', views.update_event, name='update_event'),
    path('<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('register/<int:event_id>/', views.register_event, name='register_event'),
    path('user_events/', views.user_events, name='user_events'),
]
