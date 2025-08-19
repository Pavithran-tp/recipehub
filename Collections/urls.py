from django.urls import path
from . import views
from .views import (CollectionListView,CreateCollectionView,CollectionDetailView,CollectionDeleteView,)

app_name = 'collections'

urlpatterns = [
    path('', views.CollectionListView.as_view(), name='collection-list'),
    path('create/', views.CreateCollectionView.as_view(), name='collection-create'),
    path('collection/<int:collection_id>/', views.CollectionDetailView.as_view(), name='collection-detail'),
    path('collection/<int:collection_id>/delete/', views.CollectionDeleteView.as_view(), name='collection-delete'),
]
