from django.urls import path
from . import views

app_name = 'collections'
urlpatterns = [
    path('create/', views.CreateCollectionView.as_view(), name='collection-create'),
]
