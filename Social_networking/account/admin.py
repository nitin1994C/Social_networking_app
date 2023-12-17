from django.contrib import admin
from .models import User, UserProfile, Friendship
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display =['id','email', 'is_active']
    ordering =('-date_joined',)
    filter_horizontal=()
    list_filter =()
    fieldsets=()

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
admin.site.register(Friendship)
