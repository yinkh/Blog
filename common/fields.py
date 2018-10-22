from django.forms.widgets import TextInput


class TagWidget(TextInput):
    template_name = 'widgets/tag_input.html'
