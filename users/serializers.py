from dj_rest_auth.registration.serializers import RegisterSerializer as DefaultRegisterSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

# Custom registration serializer to include extra fields (optional)
class RegisterSerializer(DefaultRegisterSerializer):
    bio = serializers.CharField(required=False)
    location = serializers.CharField(required=False)

    def custom_signup(self, request, user):
        Profile.objects.create(
            user=user,
            bio=self.validated_data.get('bio', ''),
            location=self.validated_data.get('location', '')
        )

# Serializer for Profile CRUD functionality
class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'location']
