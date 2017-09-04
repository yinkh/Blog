from django.conf.urls import url
from django.views.generic import DetailView
from .views import *

urlpatterns = [
    url(r'^$', NewsView.as_view(), name='news_index'),
    url(r'^(?P<pk>\d+)/$', NewsDetailView.as_view(), name='news_detail'),
]
