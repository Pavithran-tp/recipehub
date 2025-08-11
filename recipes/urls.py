from django.urls import path
from .views import HomeView, RecipeCreateView, RecipeDetailView, RecipeUpdateView, RecipeDeleteView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('recipes/create/', RecipeCreateView.as_view(), name='recipe_create'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipes/<int:pk>/update/', RecipeUpdateView.as_view(), name='recipe_update'),
    path('recipes/<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe_delete'),
]
