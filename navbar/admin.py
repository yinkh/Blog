from django.contrib import admin
from .models import *


class NavBarAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'url', 'order', 'create_time')
    list_filter = ('create_time',)
admin.site.register(NavBar, NavBarAdmin)
