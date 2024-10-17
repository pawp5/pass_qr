from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Event, Pass


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # Make password write-only
        }
        
    
class EventSerializer(serializers.ModelSerializer):
    attendees = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ['name', 'image', 'description', 'date', 'location', 'attendees', 'created_at', 'status']
        read_only_fields = ['attendees', 'created_at', 'status']


class PassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pass
        fields = ['event', 'user', 'qrcode', 'created_at', 'status']
        read_only_fields = ['qrcode', 'created_at', 'status']