from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Interest, User, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = 'user profile'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


admin.site.register(Interest)
admin.site.register(User, UserAdmin)
