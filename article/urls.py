from django.urls import path, include
from .views import *

urlpatterns = [
    path('', ArticleIndexView.as_view(), name='article_index'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('create/', ArticleCreateView.as_view(), name='article_create'),
    path('update/<int:pk>/', ArticleUpdateView.as_view(), name='article_update'),
    path('all/', AllView.as_view(), name='article_all'),
    path('comment/<int:pk>/', CommentControl.as_view(), name='article_comments'),

    CategoryPopupCRUDViewSet.urls(),
]
