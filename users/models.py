from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class Skill(models.Model):
    """
    A skill that can be taught or learned on SkillLoop.
    Example: 'Guitar', 'Python Basics', 'Public Speaking'.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class SkillExchange(models.Model):
    """
    Connects a user with a skill and how they want to use it
    (teach, learn, or both).
    """
    ROLE_CHOICES = (
        ("teacher", "Can teach"),
        ("learner", "Wants to learn"),
        ("both", "Can teach & learn"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="skill_exchanges",
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="exchanges",
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "skill", "role")  # one role per skill per user
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.skill.name} ({self.role})"
