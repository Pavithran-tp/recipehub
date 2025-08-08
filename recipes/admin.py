from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Recipe, Collection, Ingredient  

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

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Profile', {'fields': ('is_chef', 'bio')}),
    )
    list_display = list(UserAdmin.list_display) + ['is_chef']

admin.site.register(User, CustomUserAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Collection, CollectionAdmin)

