from django.contrib import admin
from .models import *


class LinkAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'url')
    list_filter = ('create_time',)
admin.site.register(Link, LinkAdmin)
