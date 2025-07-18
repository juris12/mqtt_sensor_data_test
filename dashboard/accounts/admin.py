from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fields = ('mqtt_username', 'mqtt_password')
    readonly_fields = ('created_at',)
    can_delete = False
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['mqtt_password'].required = True
        formset.form.base_fields['mqtt_username'].required = True
        return formset
    
class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)