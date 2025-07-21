from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fields = ('mqtt_username', 'mqtt_password', 'created_at')
    readonly_fields = ('mqtt_username', 'mqtt_password', 'created_at')
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
