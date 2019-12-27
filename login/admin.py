from django.contrib import admin

# Register your models here.
from . import models


class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'sex', 'c_time', 'has_confirmed']
    search_fields = ['name', 'email', 'c_time']
    list_filter = ['sex', 'has_confirmed', 'c_time']
    ordering = ['-c_time']
class ConfirmAdmin(admin.ModelAdmin):
    list_display = ['user','c_time','code']
    search_fields = ['user']
    list_filter = ['c_time']
    ordering = ['-c_time']

admin.site.register(models.User, UserAdmin)
admin.site.register(models.ConfirmString,ConfirmAdmin)
