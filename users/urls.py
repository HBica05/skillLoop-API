from django.urls import path, include

from .views import (
    CustomRegisterView,
    ProfileListView,
    ProfileDetailView,
    SkillListCreateView,
    SkillDetailView,
    SkillExchangeListCreateView,
    SkillExchangeDetailView,
)

urlpatterns = [
    # Auth endpoints from dj-rest-auth
    path("dj-rest-auth/", include("dj_rest_auth.urls")),
    path(
        "dj-rest-auth/registration/",
        CustomRegisterView.as_view(),
        name="custom_register",
    ),

    # Profiles
    path("profiles/", ProfileListView.as_view(), name="profile-list"),
    path("profiles/<int:pk>/", ProfileDetailView.as_view(), name="profile-detail"),

    # Skills
    path("skills/", SkillListCreateView.as_view(), name="skill-list-create"),
    path("skills/<int:pk>/", SkillDetailView.as_view(), name="skill-detail"),

    # Skill exchanges
    path(
        "exchanges/",
        SkillExchangeListCreateView.as_view(),
        name="exchange-list-create",
    ),
    path(
        "exchanges/<int:pk>/",
        SkillExchangeDetailView.as_view(),
        name="exchange-detail",
    ),
]
