from django.db import models
from django.conf import settings
from recipes.models import Recipe

class Collection(models.Model):
    """
    Model representing a user's recipe collection.
    Allows users to group favorite recipes under a common name.
    """
    name = models.CharField(
        max_length=100,
        help_text="Name of the collection."
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='collections',
        help_text="The user who owns this collection."
    )
    recipes = models.ManyToManyField(
        Recipe,
        related_name='collections',
        help_text="Recipes included in this collection."
    )

    def __str__(self):
        return f"{self.name} ({self.user.username})"
