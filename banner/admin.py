from django.contrib import admin
from .models import *


class BannerAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title', 'article', 'img', 'img_xs', 'create_time')
    list_filter = ('create_time',)
    fields = ('title', 'article', 'img', 'img_xs', 'summary')
admin.site.register(Banner, BannerAdmin)
