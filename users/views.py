from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, permissions
from .models import Profile, Skill, SkillExchange, Contact
from .serializers import (
    ProfileSerializer,
    SkillSerializer,
    SkillExchangeSerializer,
    ContactSerializer,
)
from .permissions import IsOwnerOrReadOnly


# -----------------------
# PROFILE
# -----------------------
class ProfileListView(generics.ListAPIView):
    """
    GET /api/profiles/  -> list all profiles (read-only, public)
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    GET   /api/profiles/<id>/  -> retrieve a profile
    PUT   /api/profiles/<id>/  -> update (owner only)
    PATCH /api/profiles/<id>/  -> partial update (owner only)
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class CurrentUserProfileView(generics.RetrieveUpdateAPIView):
    """
    GET   /api/profile/me/  -> get the logged-in user's own profile
    PATCH /api/profile/me/  -> update the logged-in user's own profile
    """
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


# -----------------------
# CONTACT
# -----------------------
class ContactCreateView(generics.CreateAPIView):
    """
    POST /api/contact/  -> anyone can submit a contact message
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.AllowAny]


# -----------------------
# SKILLS
# -----------------------
class SkillListCreateView(generics.ListCreateAPIView):
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Skill.objects.all()
        search = self.request.query_params.get('search', '')
        category = self.request.query_params.get('category', '')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(category__icontains=search)
            )
        if category:
            queryset = queryset.filter(category__iexact=category)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
class SkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/skills/<id>/
    PUT    /api/skills/<id>/
    PATCH  /api/skills/<id>/
    DELETE /api/skills/<id>/
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


# -----------------------
# SKILL EXCHANGES
# -----------------------
class SkillExchangeListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/exchanges/  -> list exchanges where you are requester or recipient
    POST /api/exchanges/  -> create a new exchange request
    """
    serializer_class = SkillExchangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return SkillExchange.objects.filter(
            Q(requester=user) | Q(recipient=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)


class SkillExchangeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/exchanges/<id>/
    PUT    /api/exchanges/<id>/
    PATCH  /api/exchanges/<id>/
    DELETE /api/exchanges/<id>/
    """
    queryset = SkillExchange.objects.all()
    serializer_class = SkillExchangeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]