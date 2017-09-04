from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import News


class NewsAdmin(SummernoteModelAdmin):
    search_fields = ('title', 'summary')
    list_filter = ('source', 'create_time')
    list_display = ('title', 'source', 'url', 'create_time')
admin.site.register(News, NewsAdmin)
