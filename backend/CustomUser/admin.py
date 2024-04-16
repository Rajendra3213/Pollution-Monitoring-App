from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.
class AdminUser(admin.ModelAdmin):
    list_display=['email','date_joined','last_login','is_staff','is_active']
    search_fields=['email']
    readonly_fields=['date_joined','last_login','id','password']

    filter_horizontal=[]
    list_filter=[]
    fieldsets=[]

admin.site.register(User)