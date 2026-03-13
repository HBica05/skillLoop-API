from django.urls import path

from .views import (
    ContactCreateView,
    SkillListCreateView,
    SkillDetailView,
    SkillExchangeListCreateView,
    SkillExchangeDetailView,
)

urlpatterns = [
    path("contact/", ContactCreateView.as_view(), name="contact-create"),
    path("skills/", SkillListCreateView.as_view(), name="skill-list-create"),
    path("skills/<int:pk>/", SkillDetailView.as_view(), name="skill-detail"),
    path("exchanges/", SkillExchangeListCreateView.as_view(), name="exchange-list-create"),
    path("exchanges/<int:pk>/", SkillExchangeDetailView.as_view(), name="exchange-detail"),
]