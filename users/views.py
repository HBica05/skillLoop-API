from django.contrib.auth.models import User
from rest_framework import generics, permissions

from .models import Profile, Skill, SkillExchange, Contact
from .serializers import (
    RegisterSerializer,
    ProfileSerializer,
    SkillSerializer,
    SkillExchangeSerializer,
    ContactSerializer,
)


class RegisterAPIView(generics.CreateAPIView):
    """
    Simple registration endpoint:
    - creates a User
    - creates a Profile (bio, location optional)
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # Save the user using our custom serializer
        user = serializer.save()
        bio = serializer.validated_data.get("bio", "")
        location = serializer.validated_data.get("location", "")

        # Avoid UNIQUE constraint issues
        Profile.objects.get_or_create(
            user=user,
            defaults={"bio": bio, "location": location},
        )
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
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile


class SkillListCreateView(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SkillExchangeListCreateView(generics.ListCreateAPIView):
    queryset = SkillExchange.objects.all()
    serializer_class = SkillExchangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)


class ContactCreateView(generics.CreateAPIView):
    """
    Public contact endpoint:
    - anyone can POST name, email, subject, message
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.AllowAny]


class ContactListView(generics.ListAPIView):
    """
    Admin-only list of contact messages.
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAdminUser]
