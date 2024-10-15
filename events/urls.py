from django.urls import path

from .views import get_pass


urlpatterns = [
    path('', get_pass, name='get_pass'),
]
