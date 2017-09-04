from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('create_time',)
    list_display = ('id', 'name', 'parent')
    fields = ('name', 'parent')
admin.site.register(Category, CategoryAdmin)


class ArticleAdmin(SummernoteModelAdmin):
    search_fields = ('title', 'summary',)
    list_filter = ('status', 'category', 'is_top',
                   'create_time', 'update_time', 'is_top')
    list_display = ('id', 'title', 'category', 'author', 'status', 'is_public', 'is_top', 'publish_time')
    fieldsets = (
        (u'基本信息', {
            'fields': ('title', 'tags', 'thumbnail',
                       'category', 'author', 'status',
                       'is_public', 'is_top',)
        }),
        (u'内容', {
            'fields': ('content',)
        }),
        (u'摘要', {
            'fields': ('summary',)
        }),
        (u'时间', {
            'fields': ('publish_time',)
        }),
    )
admin.site.register(Article, ArticleAdmin)


class CommentAdmin(admin.ModelAdmin):
    search_fields = ('user__username', 'article__title', 'text')
    list_filter = ('create_time',)
    list_display = ('user', 'article', 'text', 'create_time')
    fields = ('user', 'article', 'parent', 'text')
admin.site.register(Comment, CommentAdmin)

