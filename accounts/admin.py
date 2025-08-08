from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Profile', {'fields': ('is_chef', 'bio')}),
    )
    list_display = list(UserAdmin.list_display) + ['is_chef']

admin.site.register(User, CustomUserAdmin)
