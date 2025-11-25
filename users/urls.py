from django.urls import path

from .views import (
    RegisterAPIView,
    MyProfileView,
    SkillListCreateView,
    SkillExchangeListCreateView,
)

urlpatterns = [
    # POST /api/register/
    path("register/", RegisterAPIView.as_view(), name="register"),

    # GET/PUT/PATCH /api/me/
    path("me/", MyProfileView.as_view(), name="my-profile"),

    # (you'll use these later)
    path("skills/", SkillListCreateView.as_view(), name="skill-list-create"),
    path(
        "exchanges/",
        SkillExchangeListCreateView.as_view(),
        name="skill-exchange-list-create",
    ),
]
