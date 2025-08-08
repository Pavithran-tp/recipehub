from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Used to manage authentication and relate recipes to authors.
    """
    is_chef = models.BooleanField(
        default=False,
        help_text="Check if the user is a chef."
    )
    bio = models.TextField(
        blank=True,
        null=True,
        help_text="Short biography or introduction about the user."
    )
    
    # The following fields are redefined to avoid reverse accessor clashes
    # with the default auth.User model.
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username
