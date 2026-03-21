from dj_rest_auth.registration.serializers import (
    RegisterSerializer as DjRestAuthRegisterSerializer,
)
from rest_framework import serializers
from .models import Profile, Skill, SkillExchange, Contact


class RegisterSerializer(DjRestAuthRegisterSerializer):
    """
    Custom registration serializer.
    Extends dj-rest-auth's RegisterSerializer and adds optional
    profile fields (bio, location).
    """
    _has_phone_field = False
    bio = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField(required=False, allow_blank=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data["bio"] = self.validated_data.get("bio", "")
        data["location"] = self.validated_data.get("location", "")
        return data


class SkillSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Skill
        fields = [
            "id", "owner", "owner_username",
            "title", "description", "category",
            "level", "is_remote", "created_at",
        ]
        read_only_fields = ["owner", "created_at"]


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")
    # Nest the user's skills so the frontend can read them from the profile
    skills = SkillSerializer(source="user.skills", many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "user", "username", "bio", "location", "avatar", "skills"]
        read_only_fields = ["user"]


class SkillExchangeSerializer(serializers.ModelSerializer):
    requester_username = serializers.ReadOnlyField(source="requester.username")
    recipient_username = serializers.ReadOnlyField(source="recipient.username")

    class Meta:
        model = SkillExchange
        fields = [
            "id", "requester", "requester_username",
            "recipient", "recipient_username",
            "skill_offered", "skill_requested",
            "message", "status",
            "created_at", "updated_at",
        ]
        read_only_fields = ["requester", "created_at", "updated_at"]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"
        read_only_fields = ["created_at", "is_resolved"]