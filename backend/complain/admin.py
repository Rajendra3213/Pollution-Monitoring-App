from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import UserComplain

@admin.register(UserComplain)
class UserComplainAdmin(ModelAdmin):
    pass