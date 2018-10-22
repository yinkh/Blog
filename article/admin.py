from django.contrib import admin
from django.forms import ModelForm
from django_summernote.admin import SummernoteModelAdmin

from .models import *


# 保证文章的上级分类不为本分类
class CategoryAdminForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CategoryAdminForm, self).__init__(*args, **kwargs)
        if self:
            self.fields['parent'].queryset = Category.objects.exclude(id=self.instance.id)


class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    search_fields = ('name',)
    list_filter = ('create_time',)
    list_display = ('id', 'name', 'parent')
    fields = ('name', 'parent')


class ArticleAdmin(SummernoteModelAdmin):
    search_fields = ('title', 'summary',)
    list_filter = ('status', 'category', 'is_top', 'create_time', 'update_time', 'is_top')
    list_display = ('id', 'title', 'category', 'author', 'status', 'view_times', 'is_public', 'is_top', 'publish_time')
    summernote_fields = ('content',)
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'tags', 'thumbnail', 'category', 'author', 'status', 'view_times',
                       'is_public', 'is_top',)
        }),
        ('内容', {
            'fields': ('content',)
        }),
        ('摘要', {
            'fields': ('summary',)
        }),
        ('时间', {
            'fields': ('publish_time',)
        }),
    )


class CommentAdmin(admin.ModelAdmin):
    search_fields = ('user__username', 'article__title', 'text')
    list_filter = ('create_time',)
    list_display = ('user', 'article', 'text', 'create_time')
    fields = ('user', 'article', 'parent', 'text')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
