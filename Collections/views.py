from django.views.generic import (CreateView,ListView,DetailView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Collection
from recipes.models import Recipe
from .forms import CollectionForm
from django.db.models import Count

class CreateCollectionView(LoginRequiredMixin, CreateView):
    model = Collection
    form_class = CollectionForm
    template_name = 'collections/collection_form.html'
    success_url = reverse_lazy('collections:collection-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CollectionListView(LoginRequiredMixin, ListView):
    model = Collection
    template_name = 'collections/collection_list.html'
    context_object_name = 'collections'

    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user).annotate(recipes_count=Count('recipes'))


class CollectionDetailView(LoginRequiredMixin, DetailView):
    model = Collection
    template_name = 'collections/collection_detail.html'
    context_object_name = 'collection'

    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user).prefetch_related('recipes__author')
