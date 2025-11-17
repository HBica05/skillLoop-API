from dj_rest_auth.registration.serializers import (
    RegisterSerializer as DefaultRegisterSerializer,
)
from rest_framework import serializers

from .models import Profile, Skill, SkillExchange


class RegisterSerializer(DefaultRegisterSerializer):
    """
    Extends dj-rest-auth's RegisterSerializer so that when a user signs up
    we also create a Profile with optional bio & location.
    """

    bio = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField(required=False, allow_blank=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data["bio"] = self.validated_data.get("bio", "")
        data["location"] = self.validated_data.get("location", "")
        return data

    def custom_signup(self, request, user):
        # Create the Profile when the user signs up
        Profile.objects.create(
            user=user,
            bio=self.validated_data.get("bio", ""),
            location=self.validated_data.get("location", ""),
        )


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        # If you later add fields to Skill they will automatically appear
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    # user is set automatically; don’t allow the client to change it
    class Meta:
        model = Profile
        fields = ["id", "user", "bio", "location", "skills"]
        read_only_fields = ["user"]


class SkillExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillExchange
        fields = "__all__"
        # These are set by the backend, not the client
        read_only_fields = ["owner", "created_at", "updated_at"]
