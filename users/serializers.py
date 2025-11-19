from dj_rest_auth.registration.serializers import (
    RegisterSerializer as DefaultRegisterSerializer,
)
from rest_framework import serializers

from .models import Profile, Skill, SkillExchange


# -------------------------------------------------------------------
# Registration Serializer
# -------------------------------------------------------------------
class RegisterSerializer(DefaultRegisterSerializer):
    """
    Extends dj-rest-auth's RegisterSerializer so that when a user signs up,
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
        Profile.objects.create(
            user=user,
            bio=self.validated_data.get("bio", ""),
            location=self.validated_data.get("location", ""),
        )


# -------------------------------------------------------------------
# Profile Serializer
# -------------------------------------------------------------------
class ProfileSerializer(serializers.ModelSerializer):
    """
    Profile belongs to a User (One-To-One).
    We expose username instead of raw user ID.
    """

    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "user", "bio", "location", "skills", "created_at"]
        read_only_fields = ["user", "created_at"]


# -------------------------------------------------------------------
# Skill Serializer
# -------------------------------------------------------------------
class SkillSerializer(serializers.ModelSerializer):
    """
    Serializer for individual skills.
    Owner is read-only and populated automatically.
    """

    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Skill
        fields = [
            "id",
            "owner",
            "name",
            "description",
            "created_at",
        ]
        read_only_fields = ["owner", "created_at"]


# -------------------------------------------------------------------
# Skill Exchange Serializer
# -------------------------------------------------------------------
class SkillExchangeSerializer(serializers.ModelSerializer):
    """
    Serializer for Skill Exchanges.
    Automatically sets requester (owner) and timestamps.
    """

    requester = serializers.StringRelatedField(read_only=True)
    offered_skill = SkillSerializer(read_only=True)
    requested_skill = SkillSerializer(read_only=True)

    class Meta:
        model = SkillExchange
        fields = [
            "id",
            "requester",
            "offered_skill",
            "requested_skill",
            "message",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "requester",
            "created_at",
            "updated_at",
        ]
