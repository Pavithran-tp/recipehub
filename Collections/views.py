# --- Create a new file: collections/views.py ---
# This file will hold the views for the collections app.

from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Collection
from .forms import CollectionForm

class CreateCollectionView(LoginRequiredMixin, CreateView):
    """
    Allows a logged-in user to create a new, empty collection.
    """
    model = Collection
    form_class = CollectionForm
    template_name = 'collections/collection_form.html'
    success_url = reverse_lazy('recipes:home') # Redirect to the home page for now

    def form_valid(self, form):
        """
        Assigns the current user as the owner of the new collection before saving.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)
