from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        # Create and return a new `User` instance, given the validated data.
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user