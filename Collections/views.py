from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Collection
from .forms import CollectionForm

class CreateCollectionView(LoginRequiredMixin, CreateView):
    model = Collection
    form_class = CollectionForm
    template_name = 'collections/collection_form.html'
    success_url = reverse_lazy('recipes:home') 

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
