from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Extends the built-in User with extra fields used across the platform.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    avatar = models.URLField(blank=True)  # you can later swap to ImageField
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["user__username"]

    def __str__(self):
        return f"Profile({self.user.username})"


class Skill(models.Model):
    """
    A skill that a user can offer or learn.
    """
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

    LEVEL_CHOICES = [
        (BEGINNER, "Beginner"),
        (INTERMEDIATE, "Intermediate"),
        (ADVANCED, "Advanced"),
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="skills",
    )
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=120, blank=True)
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default=BEGINNER,
    )
    is_remote = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.owner.username})"


class SkillExchange(models.Model):
    """
    A request to exchange skills between two users.
    """
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    COMPLETED = "completed"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (ACCEPTED, "Accepted"),
        (DECLINED, "Declined"),
        (COMPLETED, "Completed"),
    ]

    requester = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="skill_requests_sent",
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="skill_requests_received",
    )
    skill_offered = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="offers",
    )
    skill_requested = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="requests",
    )
    message = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.requester} ↔ {self.recipient} ({self.status})"


