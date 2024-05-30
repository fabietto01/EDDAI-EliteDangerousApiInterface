from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'username', 'is_staff', 'is_active']
