from django.views.generic import (CreateView,ListView,DetailView,DeleteView,View,)
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Collection
from recipes.models import Recipe
from .forms import CollectionForm
from django.db.models import Count

class CollectionRecipeMixin(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        self.collection_id = self.kwargs.get('collection_id')
        self.recipe_id = self.kwargs.get('recipe_id')
        self.collection = get_object_or_404(Collection, id=self.collection_id, user=request.user)
        self.recipe = get_object_or_404(Recipe, id=self.recipe_id)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('recipe_collections:collection-detail', kwargs={'collection_id': self.collection_id})

class CreateCollectionView(LoginRequiredMixin, CreateView):
    model = Collection
    form_class = CollectionForm
    template_name = 'recipe_collections/collection_form.html'
    success_url = reverse_lazy('recipe_collections:collection-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CollectionListView(LoginRequiredMixin, ListView):
    model = Collection
    template_name = 'recipe_collections/collection_list.html'
    context_object_name = 'recipe_collections'

    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user).annotate(recipes_count=Count('recipes'))


class CollectionDetailView(LoginRequiredMixin, DetailView):
    model = Collection
    template_name = 'recipe_collections/collection_detail.html'
    context_object_name = 'collection'
    pk_url_kwarg = 'collection_id'

    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user).prefetch_related('recipes__author')


class CollectionDeleteView(LoginRequiredMixin, DeleteView):
    model = Collection
    template_name = 'recipe_collections/collection_confirm_delete.html'
    pk_url_kwarg = 'collection_id'
    success_url = reverse_lazy('recipe_collections:collection-list')

    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user)


class AddToCollectionView(CollectionRecipeMixin, View):
    def post(self, request, *args, **kwargs):
        self.collection.recipes.add(self.recipe)
        return redirect(self.get_success_url())


class RemoveRecipeFromCollectionView(CollectionRecipeMixin, View):
    def post(self, request, *args, **kwargs):
        self.collection.recipes.remove(self.recipe)
        return redirect(self.get_success_url())
