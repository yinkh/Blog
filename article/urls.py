from django.conf.urls import url, include
from .views import *

category_urlpatterns = [
    url(r'^popup/$', CategoryPopupCreateView.as_view(), name='category_popup_create'),
    url(r'^popup/(?P<pk>\d+)/$', CategoryPopupUpdateView.as_view(), name='category_popup_update'),
    url(r'^popup/delete/(?P<pk>\d+)/$', CategoryPopupDeleteView.as_view(), name='category_popup_delete'),
]

urlpatterns = [
    url(r'^$', ArticleIndexView.as_view(), name='article_index'),
    url(r'^(?P<pk>\d+)/$', ArticleDetailView.as_view(), name='article_detail'),
    url(r'^create/$', ArticleCreateView.as_view(), name='article_create'),
    url(r'^update/(?P<pk>\d+)/', ArticleUpdateView.as_view(), name='article_update'),
    url(r'^all/$', AllView.as_view(), name='article_all'),
    url(r'^comment/(?P<pk>\d+)/$', CommentControl.as_view(), name='article_comments'),

    url(r'^category/', include(category_urlpatterns)),
]
