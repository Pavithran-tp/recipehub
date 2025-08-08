from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Profile', {'fields': ('is_chef', 'bio')}),
    )
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Profile', {'fields': ('is_chef', 'bio')}),
    )

admin.site.register(User, CustomUserAdmin)
