from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', ArticleIndexView.as_view(), name='article_index'),
    url(r'^(?P<pk>\d+)/$', ArticleDetailView.as_view(), name='article_detail'),
    url(r'^create/$', ArticleCreateView.as_view(), name='article_create'),
    url(r'^update/(?P<pk>\d+)/', ArticleUpdateView.as_view(), name='article_update'),
    url(r'^all/$', AllView.as_view(), name='article_all'),
    url(r'^comment/(?P<pk>\d+)/$', CommentControl.as_view(), name='article_comments'),
]
