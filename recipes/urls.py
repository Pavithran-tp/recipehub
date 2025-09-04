from django.urls import path
from . import views
from .views import ( 
    RecipeListView,
    RecipeDetailView,
    CreateRecipeView,
    UpdateRecipeView,
    DeleteRecipeView,
    FeaturedRecipeView,
    SetTimezoneView
    )

app_name = 'recipes' 

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='home'),
    path('recipe/<int:recipe_id>/', views.RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipe/create/', views.CreateRecipeView.as_view(), name='recipe-create'),
    path('recipe/<int:recipe_id>/update/', views.UpdateRecipeView.as_view(), name='recipe-update'),
    path('recipe/<int:recipe_id>/delete/', views.DeleteRecipeView.as_view(), name='recipe-delete'),
    path('featured/', views.FeaturedRecipeView.as_view(), name='featured-recipes'),
    path('set-timezone/', SetTimezoneView.as_view(), name='set_timezone'),
]
