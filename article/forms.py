from django import forms
from common.fields import ForeignKeyWidget
from django.core.urlresolvers import reverse_lazy
# Summer noteWidget固定大小 Summer noteInplaceWidget 自由大小
from django_summernote.widgets import SummernoteInplaceWidget
from common.fields import TagWidget

from .models import *


# 博客表单
class ArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['status'].widget.attrs.update({'class': "form-control"})
        self.fields['tags'].widget.attrs.update({'class': 'form-control'})
        # self.fields['thumbnail'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_public'].widget.attrs.update({'type': 'checkbox'})
        self.fields['is_top'].widget.attrs.update({'type': 'checkbox'})
        self.fields['content'].widget.attrs.update({'class': 'form-control'})
        self.fields['summary'].widget.attrs.update({'class': 'form-control'})
        self.fields['publish_time'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Article
        fields = ['title', 'category', 'status', 'tags', 'thumbnail', 'is_public', 'is_top', 'content', 'summary',
                  'publish_time']
        widgets = {
            'category': ForeignKeyWidget(url_template=reverse_lazy('category_popup_create')),
            'tags': TagWidget(),
            'content': SummernoteInplaceWidget(),
        }


class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['parent'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Category
        fields = ['name', 'parent']
