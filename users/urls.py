from django.urls import path

from .views import (
    ContactCreateView,
    SkillListCreateView,
    SkillDetailView,
    SkillExchangeListCreateView,
)

urlpatterns = [
    # Contact
    path("contact/", ContactCreateView.as_view(), name="contact-create"),

    # Skills
    path("skills/", SkillListCreateView.as_view(), name="skill-list-create"),
    path("skills/<int:pk>/", SkillDetailView.as_view(), name="skill-detail"),

    # Exchanges
    path("exchanges/", SkillExchangeListCreateView.as_view(), name="exchange-list-create"),
]
