from django.forms.widgets import Select, TextInput


class ForeignKeyWidget(Select):
    template_name = 'widgets/foreign_key_select.html'

    def __init__(self, url_template, *args, **kw):
        super(ForeignKeyWidget, self).__init__(*args, **kw)
        self.url_template = url_template

    def get_context(self, name, value, attrs):
        context = super(ForeignKeyWidget, self).get_context(name, value, attrs)
        context['add_url'] = self.url_template
        context['update_url'] = self.url_template
        context['delete_url'] = self.url_template + 'delete/'
        return context


class TagWidget(TextInput):
    template_name = 'widgets/tag_input.html'
