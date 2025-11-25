from dj_rest_auth.registration.serializers import (
    RegisterSerializer as DjRestAuthRegisterSerializer,
)
from rest_framework import serializers

from .models import Profile, Skill, SkillExchange


class RegisterSerializer(DjRestAuthRegisterSerializer):
    """
    Custom registration serializer.
    Extends dj-rest-auth's RegisterSerializer and adds optional
    profile fields (bio, location).
    """

    # Explicitly say there is NO phone field, to avoid '_has_phone_field' errors
    _has_phone_field = False

    bio = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField(required=False, allow_blank=True)

    def get_cleaned_data(self):
        """
        Called by dj-rest-auth when creating the User.
        We add 'bio' and 'location' to the cleaned data dict.
        """
        data = super().get_cleaned_data()
        data["bio"] = self.validated_data.get("bio", "")
        data["location"] = self.validated_data.get("location", "")
        return data


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "user", "bio", "location", "avatar", "skills"]
        read_only_fields = ["user"]


class SkillExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillExchange
        fields = "__all__"
        read_only_fields = ["owner", "created_at", "updated_at"]
