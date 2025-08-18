from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import QuerySet
from .models import Recipe, Ingredient, Collection, VegType, DifficultyLevel, CuisineType, Unit
from .forms import RecipeForm, IngredientForm
from django.db import transaction


User = get_user_model()

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.recipe = Recipe.objects.create(
            title='Spaghetti Carbonara',
            instructions='Cook pasta, mix with eggs...',
            cuisine=CuisineType.ITALIAN,
            difficulty=DifficultyLevel.EASY,
            veg_type=VegType.NON_VEGETARIAN,
            prep_time=15,
            total_time=30,
            calories=600,
            author=self.user
        )
        self.ingredient = Ingredient.objects.create(
            name='Pasta',
            quantity=500.00,
            unit=Unit.GRAMS,
            recipe=self.recipe
        )

    def test_recipe_model_str(self):
        self.assertEqual(str(self.recipe), 'Spaghetti Carbonara')

    def test_ingredient_model_str(self):
        self.assertEqual(str(self.ingredient), '500.00 Grams Pasta')

    def test_collection_model_str(self):
        collection = Collection.objects.create(
            name='Italian Favorites',
            user=self.user
        )
        self.assertEqual(str(collection), 'Italian Favorites (testuser)')

    def test_recipe_fields(self):
        recipe_from_db = Recipe.objects.get(pk=self.recipe.pk)
        self.assertEqual(recipe_from_db.title, 'Spaghetti Carbonara')
        self.assertEqual(recipe_from_db.author, self.user)
        self.assertEqual(recipe_from_db.prep_time, 15)
        self.assertEqual(recipe_from_db.difficulty, 'easy')
        self.assertFalse(recipe_from_db.image)

    def test_ingredient_fields(self):
        ingredient_from_db = Ingredient.objects.get(pk=self.ingredient.pk)
        self.assertEqual(ingredient_from_db.name, 'Pasta')
        self.assertEqual(ingredient_from_db.quantity, 500.00)
        self.assertEqual(ingredient_from_db.unit, 'g')
        self.assertFalse(ingredient_from_db.optional)
        self.assertEqual(ingredient_from_db.recipe, self.recipe)
        self.assertIsInstance(ingredient_from_db.recipe, Recipe)

    def test_collection_m2m(self):
        collection = Collection.objects.create(
            name='My Recipes',
            user=self.user
        )
        collection.recipes.add(self.recipe)
        self.assertIn(self.recipe, collection.recipes.all())
        self.assertIsInstance(collection.recipes.all(), QuerySet)


class FormTests(TestCase):
    def test_recipe_form_valid_data(self):
        form_data = {
            'title': 'Test Recipe',
            'cuisine': 'indian',
            'difficulty': 'medium',
            'veg_type': 'veg',
            'prep_time': 20,
            'total_time': 45,
            'instructions': 'Test instructions.',
        }
        form = RecipeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_recipe_form_invalid_data(self):
        form_data = {
            'title': '', 
            'cuisine': 'indian',
        }
        form = RecipeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_ingredient_form_valid_data(self):
        form_data = {
            'name': 'Onion',
            'quantity': 2.0,
            'unit': 'pcs',
            'optional': False,
        }
        form = IngredientForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_ingredient_form_invalid_data(self):
        form_data = {
            'name': '',
            'quantity': 2.0,
        }
        form = IngredientForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            password='password1'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='password2'
        )
        self.recipe1 = Recipe.objects.create(
            title='Penne Arrabiata',
            cuisine=CuisineType.ITALIAN,
            difficulty=DifficultyLevel.EASY,
            veg_type=VegType.VEGETARIAN,
            prep_time=10,
            total_time=25,
            instructions='...',
            author=self.user1
        )
        self.recipe2 = Recipe.objects.create(
            title='Chicken Tikka Masala',
            cuisine=CuisineType.INDIAN,
            difficulty=DifficultyLevel.MEDIUM,
            veg_type=VegType.NON_VEGETARIAN,
            prep_time=30,
            total_time=60,
            instructions='...',
            author=self.user2
        )
        self.recipe_list_url = reverse('recipes:home')
        self.recipe_detail_url = reverse('recipes:recipe-detail', kwargs={'recipe_id': self.recipe1.pk})
        self.create_recipe_url = reverse('recipes:recipe-create')
        self.update_recipe_url = reverse('recipes:recipe-update', kwargs={'recipe_id': self.recipe1.pk})
        self.delete_recipe_url = reverse('recipes:recipe-delete', kwargs={'recipe_id': self.recipe1.pk})

    def test_recipe_list_view_get(self):
        response = self.client.get(self.recipe_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_list.html')
        self.assertContains(response, 'Penne Arrabiata')
        self.assertContains(response, 'Chicken Tikka Masala')

    def test_recipe_list_view_filter_search(self):
        response = self.client.get(self.recipe_list_url, {'q': 'Penne'})
        self.assertContains(response, 'Penne Arrabiata')
        self.assertNotContains(response, 'Chicken Tikka Masala')

    def test_recipe_list_view_filter_cuisine(self):
        response = self.client.get(self.recipe_list_url, {'cuisine': 'indian'})
        self.assertContains(response, 'Chicken Tikka Masala')
        self.assertNotContains(response, 'Penne Arrabiata')

    def test_recipe_detail_view_get(self):
        response = self.client.get(self.recipe_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_detail.html')
        self.assertContains(response, 'Penne Arrabiata')

    def test_recipe_detail_view_get_404(self):
        invalid_url = reverse('recipes:recipe-detail', kwargs={'recipe_id': 999})
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 404)

    def test_create_recipe_view_unauthenticated_user(self):
        response = self.client.get(self.create_recipe_url)
        self.assertRedirects(response, f'/accounts/login/?next={self.create_recipe_url}')

    def test_create_recipe_view_get(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(self.create_recipe_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_form.html')

    def test_update_recipe_view_unauthorized_user(self):
        self.client.login(username='user2', password='password2')
        response = self.client.get(self.update_recipe_url)
        self.assertEqual(response.status_code, 403)

    def test_update_recipe_view_get_author(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(self.update_recipe_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_form.html')
        self.assertContains(response, 'Penne Arrabiata')

    def test_delete_recipe_view_unauthorized_user(self):
        self.client.login(username='user2', password='password2')
        response = self.client.get(self.delete_recipe_url)
        self.assertEqual(response.status_code, 403)

    def test_delete_recipe_view_post_author(self):
        self.client.login(username='user1', password='password1')
        initial_recipe_count = Recipe.objects.count()
        response = self.client.post(self.delete_recipe_url, follow=True)
        self.assertRedirects(response, self.recipe_list_url)
        self.assertEqual(Recipe.objects.count(), initial_recipe_count - 1)
        with self.assertRaises(Recipe.DoesNotExist):
            Recipe.objects.get(pk=self.recipe1.pk)
