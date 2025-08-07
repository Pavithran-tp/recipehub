from django.contrib import admin
from .models import User,Recipe, Collection, Ingredient  # Add your models here

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'cuisine', 'difficulty', 'veg_type', 'author', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('cuisine', 'difficulty', 'veg_type')

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'unit', 'optional', 'recipe')
    search_fields = ('name',)

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', 'user__username')
    filter_horizontal = ('recipes',)

admin.site.register(User)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Collection, CollectionAdmin)

