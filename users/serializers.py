from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User
from dj_rest_auth.registration.serializers import RegisterSerializer as DefaultRegisterSerializer

class RegisterSerializer(DefaultRegisterSerializer):
    bio = serializers.CharField(required=False)
    location = serializers.CharField(required=False)

    def get_cleaned_data(self):
        cleaned_data = super().get_cleaned_data()
        cleaned_data['bio'] = self.validated_data.get('bio', '')
        cleaned_data['location'] = self.validated_data.get('location', '')
        return cleaned_data

    def custom_signup(self, request, user):
        Profile.objects.create(
            user=user,
            bio=self.validated_data.get('bio', ''),
            location=self.validated_data.get('location', '')
        )

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'location']
