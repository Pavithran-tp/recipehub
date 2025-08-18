from django.urls import path
from . import views

app_name = 'collections'
urlpatterns = [
    path('', views.CollectionListView.as_view(), name='collection-list'),
    path('create/', views.CreateCollectionView.as_view(), name='collection-create'),
    path('collection/<int:pk>/', views.CollectionDetailView.as_view(), name='collection-detail'),
]
