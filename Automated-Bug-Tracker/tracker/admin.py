from django.contrib import admin
from .models import User, Bug
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('role',)}),)

admin.site.register(User, CustomUserAdmin)