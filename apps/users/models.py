import uuid
from apps.users.managers import CustomUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.models import HistorizedModel


class CustomUser(AbstractUser, HistorizedModel):
    class Roles(models.TextChoices):
        USER = "user"
        ADMIN = "admin"

    user_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    passport_identifier = models.CharField(max_length=14)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=5, choices=Roles.choices)
    is_deleted = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    def __str__(self):
        return self.user_uuid
