from django import forms

# Summer noteWidget固定大小 Summer noteInplaceWidget 自由大小
from django_summernote.widgets import SummernoteInplaceWidget

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
            'content': SummernoteInplaceWidget(),
        }
