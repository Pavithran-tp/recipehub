from django.views.generic import (CreateView,ListView,DetailView,DeleteView,View,)
from django.shortcuts import redirect, get_object_or_404
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
    pk_url_kwarg = 'collection_id'

    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user).prefetch_related('recipes__author')


class CollectionDeleteView(LoginRequiredMixin, DeleteView):
    model = Collection
    template_name = 'collections/collection_confirm_delete.html'
    pk_url_kwarg = 'collection_id'
    success_url = reverse_lazy('collections:collection-list')

    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user)


class AddToCollectionView(LoginRequiredMixin, View):
    def post(self, request, collection_id, recipe_id, *args, **kwargs):
        collection = get_object_or_404(Collection, id=collection_id, user=request.user)
        recipe = get_object_or_404(Recipe, id=recipe_id)
        collection.recipes.add(recipe)
        return redirect('collections:collection-detail', collection_id=collection_id)


class RemoveRecipeFromCollectionView(LoginRequiredMixin, View):
    def post(self, request, collection_id, recipe_id, *args, **kwargs):
        collection = get_object_or_404(Collection, id=collection_id, user=request.user)
        recipe = get_object_or_404(Recipe, id=recipe_id)
        collection.recipes.remove(recipe)
        return redirect('collections:collection-detail', collection_id=collection_id)

