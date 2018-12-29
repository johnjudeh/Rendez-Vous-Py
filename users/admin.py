from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Interest, User

admin.site.register(Interest)
admin.site.register(User, UserAdmin)