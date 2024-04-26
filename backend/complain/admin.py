from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import UserComplain,ValidationAuthority

@admin.register(UserComplain)
class UserComplainAdmin(ModelAdmin):
    list_display=['id','severity_level','date_of_complain','solved','validated_by']
    list_filter = ['solved', 'severity_level']

@admin.register(ValidationAuthority)
class ValidationAuthorityAdmin(ModelAdmin):
    list_display=['id','name','contact']