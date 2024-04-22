from django.contrib import admin
from .models import User,EmailConfirm
from unfold.admin import ModelAdmin
from django.contrib.auth.models import Group

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(ModelAdmin):
    pass

@admin.register(EmailConfirm)
class EmailAdmin(ModelAdmin):
    pass