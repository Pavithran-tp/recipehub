from django.urls import path
from . import views
from .views import (CollectionListView, CreateCollectionView, CollectionDetailView, CollectionDeleteView, AddToCollectionView, RemoveRecipeFromCollectionView,)

app_name = 'collections'

urlpatterns = [
    path('', views.CollectionListView.as_view(), name='collection-list'),
    path('create/', views.CreateCollectionView.as_view(), name='collection-create'),
    path('collection/<int:collection_id>/', views.CollectionDetailView.as_view(), name='collection-detail'),
    path('collection/<int:collection_id>/delete/', views.CollectionDeleteView.as_view(), name='collection-delete'),
    path('add-recipe/<int:collection_id>/<int:recipe_id>/', views.AddToCollectionView.as_view(), name='add-recipe-to-collection'),
    path('remove-recipe/<int:collection_id>/<int:recipe_id>/', views.RemoveRecipeFromCollectionView.as_view(), name='remove-recipe-from-collection'),
]
