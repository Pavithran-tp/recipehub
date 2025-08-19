from django.urls import path
from .views import (CollectionListView, CreateCollectionView, CollectionDetailView, CollectionDeleteView, AddToCollectionView, RemoveRecipeFromCollectionView,)

app_name = 'collections'


urlpatterns = [
    path('', CollectionListView.as_view(), name='collection-list'),
    path('create/', CreateCollectionView.as_view(), name='collection-create'),
    path('collection/<int:collection_id>/', CollectionDetailView.as_view(), name='collection-detail'),
    path('collection/<int:collection_id>/delete/', CollectionDeleteView.as_view(), name='collection-delete'),
    path('add-recipe/<int:collection_id>/<int:recipe_id>/', AddToCollectionView.as_view(), name='add-recipe-to-collection'),
    path('remove-recipe/<int:collection_id>/<int:recipe_id>/', RemoveRecipeFromCollectionView.as_view(), name='remove-recipe-from-collection'),
]
