from django.urls import path
from .views import (
    RegisterAPIView,
    MyProfileView,
    SkillListCreateView,
    SkillExchangeListCreateView,
    ContactCreateView,
    ContactListView,
)

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("me/", MyProfileView.as_view(), name="my-profile"),
    path("skills/", SkillListCreateView.as_view(), name="skill-list-create"),
    path(
        "skill-exchanges/",
        SkillExchangeListCreateView.as_view(),
        name="skill-exchange-list-create",
    ),
    path("contact/", ContactCreateView.as_view(), name="contact-create"),
    path("contact/messages/", ContactListView.as_view(), name="contact-list"),
]
