from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission


# Class-based choices
class VegType(models.TextChoices):
    VEGETARIAN = 'veg', 'Vegetarian'
    NON_VEGETARIAN = 'non_veg', 'Non-Vegetarian'
    VEGAN = 'vegan', 'Vegan'


class DifficultyLevel(models.TextChoices):
    EASY = 'easy', 'Easy'
    MEDIUM = 'medium', 'Medium'
    HARD = 'hard', 'Hard'


class CuisineType(models.TextChoices):
    INDIAN = 'indian', 'Indian'
    ITALIAN = 'italian', 'Italian'
    CHINESE = 'chinese', 'Chinese'
    MEXICAN = 'mexican', 'Mexican'
    OTHER = 'other', 'Other'

class Unit(models.TextChoices):
    GRAMS = 'g', 'Grams'
    KILOGRAMS = 'kg', 'Kilograms'
    MILLILITERS = 'ml', 'Milliliters'
    LITERS = 'l', 'Liters'
    TEASPOON = 'tsp', 'Teaspoon'
    TABLESPOON = 'tbsp', 'Tablespoon'
    CUP = 'cup', 'Cup'
    PIECES = 'pcs', 'Pieces'


class Recipe(models.Model):
    """
    Model representing a recipe created by a user.
    Includes details like title, cuisine type, difficulty, and vegetarian option.
    """
    title = models.CharField(
        max_length=100,
        help_text="Enter the title of the recipe."
    )
    description = models.TextField(
        help_text="Provide a short description of the recipe."
    )
    cuisine = models.CharField(
        max_length=20,
        choices=CuisineType.choices,
        help_text="Select the cuisine category for the recipe."
    )
    difficulty = models.CharField(
        max_length=10,
        choices=DifficultyLevel.choices,
        help_text="Select how difficult the recipe is to prepare."
    )
    veg_type = models.CharField(
        max_length=10,
        choices=VegType.choices,
        help_text="Choose the vegetarian type of the recipe (veg, non-veg, vegan)."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when the recipe was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="The date and time when the recipe was last updated."
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipes',
        help_text="The user who created this recipe."
    )
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    instructions = models.TextField(
        default="No instructions provided.",
        help_text="Step-by-step preparation instructions."
    )
    prep_time = models.PositiveIntegerField(
        default=0,
        help_text="Preparation time in minutes."
    )
    total_time = models.PositiveIntegerField(
        default=0,
        help_text="Total time in minutes."
    )
    servings = models.PositiveIntegerField(
        default=1,
        help_text="Number of servings."
    )
    calories = models.PositiveIntegerField(
        default=0,
        help_text="Calories per serving."
    )


    def __str__(self):
        return self.title


class Ingredient(models.Model):
    """
    Model representing an ingredient used in a recipe.
    Stores the name, quantity, unit, and whether it's optional.
    """

    name = models.CharField(
        max_length=100,
        help_text="Name of the ingredient."
    )
    quantity = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    help_text="Quantity of the ingredient required for the recipe."
    )
    unit = models.CharField(
    max_length=10,
    choices=Unit.choices,
    help_text="Measurement unit for the ingredient."
    )
    optional = models.BooleanField(
        default=False,
        help_text="Check if the ingredient is optional."
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
        help_text="The recipe to which this ingredient belongs."
    )

    def __str__(self):
        return f"{self.quantity} {self.get_unit_display()} {self.name}"


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
