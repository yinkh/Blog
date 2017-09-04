from django_filters import FilterSet
from .models import *


class ArticleFilter(FilterSet):
    class Meta:
        model = Article
        fields = {
            'author': ['exact'],
            'category': ['exact'],
            'title': ['exact', 'icontains'],
            'is_public': ['exact'],
            'tags': ['exact', 'icontains'],
            'column': ['exact'],
        }
