from django.shortcuts import render
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Recipe
from .forms import RecipeForm, IngredientFormSet
from django.views.generic import ListView
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.forms import inlineformset_factory
from .models import Recipe, Ingredient
from .forms import RecipeForm, IngredientFormSet

class HomeView(ListView):
    model = Recipe
    template_name = 'recipes/home.html'  
    context_object_name = 'recipes'

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'  
    context_object_name = 'recipes'
    ordering = ['-created_at']  

class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/update_recipe.html'
    success_url = reverse_lazy('recipe_list')

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
        if form.is_valid() and ingredient_formset.is_valid():
            self.object = form.save()
            ingredient_formset.instance = self.object
            ingredient_formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def test_func(self):
        recipe = self.get_object()
        return recipe.author == self.request.user

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.pk})

class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = 'recipes/delete_recipe.html'
    success_url = reverse_lazy('recipe_list')  

    def test_func(self):
        recipe = self.get_object()
        return recipe.author == self.request.user


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/create_recipe.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['ingredient_formset'] = IngredientFormSet(self.request.POST)
        else:
            data['ingredient_formset'] = IngredientFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        ingredient_formset = context['ingredient_formset']
        form.instance.author = self.request.user
        if form.is_valid() and ingredient_formset.is_valid():
            self.object = form.save()
            ingredient_formset.instance = self.object
            ingredient_formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.pk})


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'


