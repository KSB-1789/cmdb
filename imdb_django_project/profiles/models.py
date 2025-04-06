from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    groups = models.ManyToManyField(
        "auth.Group", verbose_name=_("groups"), blank=True, related_name="user_groups"
    )
    user_permissions = models.ManyToManyField("auth.Permission", verbose_name=_("user permissions"), blank=True, related_name="user_permissions_set")

    def __str__(self):
        return self.username
