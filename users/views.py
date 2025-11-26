from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework import generics, permissions

from .models import Skill, SkillExchange, Contact
from .serializers import (
    SkillSerializer,
    SkillExchangeSerializer,
    ContactSerializer,
)
from .permissions import IsOwnerOrReadOnly


# -----------------------
# CONTACT
# -----------------------
class ContactCreateView(generics.CreateAPIView):
    """
    Public contact endpoint:
    - anyone can POST name, email, subject, message
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.AllowAny]


# -----------------------
# SKILLS
# -----------------------
class SkillListCreateView(generics.ListCreateAPIView):
    """
    GET /api/skills/  -> list all skills
    POST /api/skills/ -> create a new skill for current user
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]


# -----------------------
# SKILL EXCHANGES
# -----------------------
class SkillExchangeListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/exchanges/ -> list exchanges where you are requester or recipient
    POST /api/exchanges/ -> create a new exchange request
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
