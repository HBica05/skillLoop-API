from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from .models import Profile, Skill, SkillExchange
from .serializers import (
    ProfileSerializer,
    SkillSerializer,
    SkillExchangeSerializer,
)


# -------------------------------------------------------------------
# Permissions
# -------------------------------------------------------------------
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Only allow owners of an object to edit it.
    Everyone can read (GET, HEAD, OPTIONS).
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # For our models, "owner" / "requester" / "user" represent the owner
        owner = getattr(obj, "owner", None) or getattr(obj, "requester", None) or getattr(
            obj, "user", None
        )

        return owner == request.user


# -------------------------------------------------------------------
# Profile views
# -------------------------------------------------------------------
class MyProfileView(generics.RetrieveUpdateAPIView):
    """
    Retrieve & update the currently logged-in user's profile.
    URL: /api/profile/me/
    """

    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return self.request.user.profile
        except Profile.DoesNotExist:
            # In theory signals create it, but just in case:
            raise PermissionDenied("Profile does not exist for this user.")


# (Optional) List all profiles – e.g. for discovery.
class ProfileListView(generics.ListAPIView):
    """
    Public read-only list of profiles (no editing here).
    URL: /api/profiles/
    """

    queryset = Profile.objects.select_related("user").prefetch_related("skills")
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]


# -------------------------------------------------------------------
# Skill views
# -------------------------------------------------------------------
class SkillListCreateView(generics.ListCreateAPIView):
    """
    List all skills (GET) or create a new skill for the current user (POST).
    URL: /api/skills/
    """

    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Everyone can see all skills for now
        return Skill.objects.select_related("owner").all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a single skill.
    URL: /api/skills/<id>/
    """

    queryset = Skill.objects.select_related("owner").all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


# -------------------------------------------------------------------
# SkillExchange views
# -------------------------------------------------------------------
class SkillExchangeListCreateView(generics.ListCreateAPIView):
    """
    List exchanges (only those involving the current user) and create new ones.
    URL: /api/exchanges/
    """

    serializer_class = SkillExchangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Only show exchanges where the user is the requester
        # (you could expand this later to show "other side" too)
        return SkillExchange.objects.filter(requester=user).select_related(
            "requester", "offered_skill", "requested_skill"
        )

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)


class SkillExchangeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a single exchange, only if you are the requester.
    URL: /api/exchanges/<id>/
    """

    queryset = SkillExchange.objects.select_related(
        "requester", "offered_skill", "requested_skill"
    )
    serializer_class = SkillExchangeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
