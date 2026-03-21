from django.urls import path
from .views import (
    ContactCreateView,
    ProfileListView,
    ProfileDetailView,
    CurrentUserProfileView,
    SkillListCreateView,
    SkillDetailView,
    SkillExchangeListCreateView,
    SkillExchangeDetailView,
)

urlpatterns = [
    # Profiles
    path("profiles/", ProfileListView.as_view(), name="profile-list"),
    path("profiles/<int:pk>/", ProfileDetailView.as_view(), name="profile-detail"),
    path("profile/me/", CurrentUserProfileView.as_view(), name="profile-me"),

    # Contact
    path("contact/", ContactCreateView.as_view(), name="contact-create"),

    # Skills
    path("skills/", SkillListCreateView.as_view(), name="skill-list-create"),
    path("skills/<int:pk>/", SkillDetailView.as_view(), name="skill-detail"),

    # Exchanges
    path("exchanges/", SkillExchangeListCreateView.as_view(), name="exchange-list-create"),
    path("exchanges/<int:pk>/", SkillExchangeDetailView.as_view(), name="exchange-detail"),
]