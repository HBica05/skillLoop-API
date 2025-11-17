from dj_rest_auth.registration.views import RegisterView as DefaultRegisterView
from rest_framework import generics, permissions

from .models import Profile, Skill, SkillExchange
from .serializers import (
    RegisterSerializer,
    ProfileSerializer,
    SkillSerializer,
    SkillExchangeSerializer,
)

# Try to use your custom permission if it exists, otherwise fall back
try:
    from .permissions import IsOwnerOrReadOnly
except ImportError:  # simple fallback
    IsOwnerOrReadOnly = permissions.IsAuthenticatedOrReadOnly


class CustomRegisterView(DefaultRegisterView):
    """
    Use our extended RegisterSerializer so a Profile is created at signup.
    """
    serializer_class = RegisterSerializer


# -------- Profiles --------

class ProfileListView(generics.ListAPIView):
    """
    List all profiles (read-only). Good for browsing users.
    """
    queryset = Profile.objects.all().select_related("user").prefetch_related("skills")
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View / update / delete a single profile.
    Only the owner should be allowed to edit/delete.
    """
    queryset = Profile.objects.all().select_related("user").prefetch_related("skills")
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        # Ensure the profile always belongs to the logged-in user
        serializer.save(user=self.request.user)


# -------- Skills --------

class SkillListCreateView(generics.ListCreateAPIView):
    """
    Everyone can list skills; logged-in users can add new ones.
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve/update/delete a single skill.
    (You can later tighten permissions if needed.)
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# -------- Skill Exchanges --------

class SkillExchangeListCreateView(generics.ListCreateAPIView):
    """
    List all exchanges or create a new one.
    Owner is set automatically from the logged-in user.
    """
    queryset = SkillExchange.objects.all().select_related("owner")
    serializer_class = SkillExchangeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SkillExchangeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve/update/delete a single exchange.
    Only the owner should be allowed to modify it.
    """
    queryset = SkillExchange.objects.all().select_related("owner")
    serializer_class = SkillExchangeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
