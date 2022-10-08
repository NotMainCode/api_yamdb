"""Database settings of the 'Users' application."""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Modified model User."""

    ROLE_OPTIONS = (
        ("user", "User"),
        ("moderator", "Moderator"),
        ("admin", "Admin"),
    )
    role = models.CharField(
        "Role", max_length=9, choices=ROLE_OPTIONS, default="user"
    )
    email = models.EmailField(blank=False, unique=True)
    first_name = models.CharField("First name", max_length=150, blank=True)
    bio = models.TextField("Biography", blank=True)
    confirmation_code = models.CharField(
        "First name", max_length=32, blank=True
    )

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["username"]
