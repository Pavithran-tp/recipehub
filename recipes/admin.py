from django.contrib import admin
from .models import Recipe,Ingredient  

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'cuisine', 'difficulty', 'veg_type', 'author', 'created_at', 'featured')
    list_editable = ('featured',)
    search_fields = ('title', 'description')
    list_filter = ('cuisine', 'difficulty', 'veg_type', 'featured')

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'unit', 'optional', 'recipe')
    search_fields = ('name',)

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
