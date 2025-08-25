from django.contrib import admin
from .models import Collection

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', 'user__username')
    filter_horizontal = ('recipes',)

admin.site.register(Collection, CollectionAdmin)
