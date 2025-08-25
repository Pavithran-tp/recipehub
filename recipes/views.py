from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.forms import inlineformset_factory
from .models import Recipe, Ingredient
from .forms import RecipeForm, IngredientForm
from recipe_collections.models import Collection


IngredientFormSet = inlineformset_factory(
    Recipe,
    Ingredient,
    form=IngredientForm,
    fields=('name', 'quantity', 'unit'),
    extra=1,
    can_delete=True
)

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 9
    ordering = ['-created_at']

    @staticmethod
    def _get_recipe_filter_context(request):
        context = {}
        context['cuisine_choices'] = Recipe._meta.get_field('cuisine').choices
        context['difficulty_choices'] = Recipe._meta.get_field('difficulty').choices
        context['veg_type_choices'] = Recipe._meta.get_field('veg_type').choices
        
        context['current_filters'] = {
            'q': request.GET.get('q', ''),
            'cuisine': request.GET.get('cuisine', ''),
            'difficulty': request.GET.get('difficulty', ''),
            'veg_type': request.GET.get('veg_type', ''),
        }
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(title__icontains=query)

        cuisine = self.request.GET.get('cuisine')
        if cuisine:
            queryset = queryset.filter(cuisine=cuisine)

        difficulty = self.request.GET.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        veg_type = self.request.GET.get('veg_type')
        if veg_type:
            queryset = queryset.filter(veg_type=veg_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self._get_recipe_filter_context(self.request))
        return context


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'
    
    def get_object(self):
        return get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            from recipe_collections.models import Collection
            context['recipe_collections'] = Collection.objects.filter(user=self.request.user)
        return context


class CreateRecipeView(LoginRequiredMixin,CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'
    success_url = reverse_lazy('recipes:home')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['ingredient_formset'] = IngredientFormSet(self.request.POST, self.request.FILES, prefix='ingredient_set')
        else:
            data['ingredient_formset'] = IngredientFormSet(prefix='ingredient_set')
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        ingredient_formset = context['ingredient_formset']

        with transaction.atomic():
            if ingredient_formset.is_valid():
                self.object = form.save(commit=False)
                self.object.author = self.request.user
                self.object.save()
                ingredient_formset.instance = self.object
                ingredient_formset.save()
                return super().form_valid(form)
            else:
                return self.render_to_response(self.get_context_data(form=form))


class UpdateRecipeView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'
    
    def get_object(self):
        return get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))
    
    def get_success_url(self):
        return reverse_lazy('recipes:recipe-detail', kwargs={'recipe_id': self.object.pk})

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['ingredient_formset'] = IngredientFormSet(self.request.POST, instance=self.object)
        else:
            data['ingredient_formset'] = IngredientFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        ingredient_formset = context['ingredient_formset']

        with transaction.atomic():
            if form.is_valid() and ingredient_formset.is_valid():
                self.object = form.save()
                ingredient_formset.instance = self.object
                ingredient_formset.save()
                return redirect(self.get_success_url())
            else:
                return self.render_to_response(self.get_context_data(form=form, ingredient_formset=ingredient_formset))

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author


class DeleteRecipeView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = 'recipes/recipe_confirm_delete.html'
    success_url = reverse_lazy('recipes:home')
    
    def get_object(self):
        return get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author

class FeaturedRecipeView(ListView):
    template_name = 'recipes/featured_recipes.html'
    context_object_name = 'featured_recipes'
    paginate_by = 9

    def get_queryset(self):
        return Recipe.objects.filter(featured=True).order_by('-updated_at')
