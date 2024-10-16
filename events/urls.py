from django.urls import path

from .views import *


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('events/', event_list_create, name='event-list-create'),
    path('events/<int:pk>/', event_detail, name='event-detail'),
    path('events/<int:pk>/pass/', pass_create, name='pass-create'),
]
