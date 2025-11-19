from django.urls import path

from .views import (
    MyProfileView,
    ProfileListView,
    SkillListCreateView,
    SkillDetailView,
    SkillExchangeListCreateView,
    SkillExchangeDetailView,
)

urlpatterns = [
    # Profiles
    path("profile/me/", MyProfileView.as_view(), name="my-profile"),
    path("profiles/", ProfileListView.as_view(), name="profile-list"),

    # Skills
    path("skills/", SkillListCreateView.as_view(), name="skill-list-create"),
    path("skills/<int:pk>/", SkillDetailView.as_view(), name="skill-detail"),

    # Skill exchanges
    path(
        "exchanges/",
        SkillExchangeListCreateView.as_view(),
        name="skill-exchange-list-create",
    ),
    path(
        "exchanges/<int:pk>/",
        SkillExchangeDetailView.as_view(),
        name="skill-exchange-detail",
    ),
]
