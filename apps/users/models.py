import uuid
from apps.users.managers import CustomUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from utils.models import HistorizedModel


class CustomUser(AbstractBaseUser, PermissionsMixin, HistorizedModel):
    class Roles(models.TextChoices):
        USER = "user"
        ADMIN = "admin"

    user_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    passport_identifier = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=5, choices=Roles.choices)
    is_deleted = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'passport_identifier'

    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return str(self.user_uuid)
