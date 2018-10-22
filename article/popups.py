from django import forms
from popup_field.views import PopupCRUDViewSet

from .models import *


class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['parent'].widget.attrs.update({'class': 'form-control'})
        if self.instance:
            self.fields['parent'].queryset = Category.objects.exclude(id=self.instance.id)

    class Meta:
        model = Category
        fields = ['name', 'parent']


class CategoryPopupCRUDViewSet(PopupCRUDViewSet):
    model = Category
    form_class = CategoryForm
    template_name_create = 'popup/category/create.html'
    template_name_update = 'popup/category/update.html'
    template_name_fk = 'popup/foreign_key_select.html'
