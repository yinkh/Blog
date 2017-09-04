from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import *


class ColumnAdmin(SummernoteModelAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'create_time')
    list_filter = ('create_time',)
    fields = ('name', 'article', 'summary')
    filter_horizontal = ('article',)
admin.site.register(Column, ColumnAdmin)
