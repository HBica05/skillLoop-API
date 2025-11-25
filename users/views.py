from django.contrib.auth.models import User
from rest_framework import generics, permissions

from .models import Profile, Skill, SkillExchange
from .serializers import (
    RegisterSerializer,
    ProfileSerializer,
    SkillSerializer,
    SkillExchangeSerializer,
)


class RegisterAPIView(generics.CreateAPIView):
    """
    Simple registration endpoint:
    - creates a User
    - creates a Profile (bio, location optional)
    - returns a token (handled by dj-rest-auth)
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # IMPORTANT: pass request to save(), so dj-rest-auth/allauth
        # can run custom_signup and related logic correctly.
        user = serializer.save(request=self.request)
        return user


class MyProfileView(generics.RetrieveUpdateAPIView):
    """
    Get or update the currently logged-in user's profile.
    GET /api/me/
    PUT/PATCH /api/me/
    """
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Ensure the user always has a profile
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile


class SkillListCreateView(generics.ListCreateAPIView):
    """
    List all skills, or create a new skill for the logged-in user.
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SkillExchangeListCreateView(generics.ListCreateAPIView):
    """
    List all skill exchanges, or create a new one.
    """
    queryset = SkillExchange.objects.all()
    serializer_class = SkillExchangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)
