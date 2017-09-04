from django.db.models import Q
from common.views import BaseContextMixin
from django.views.generic import ListView
from django.conf import settings
from django.http import Http404

from article.models import Article
from article.filters import ArticleFilter
from .models import *


class ColumnView(BaseContextMixin, ListView):
    queryset = Column.objects.all()
    template_name = 'column/column.html'
    paginate_by = settings.PAGE_NUM

    def get_object(self):
        pk = self.kwargs.get('pk', '')
        try:
            return Column.objects.get(pk=pk)
        except Column.DoesNotExist:
            raise Http404

    def get_articles(self):
        if self.request.user.has_perm('article.view_article'):
            articles = Article.objects.all()
        else:
            articles = Article.public.filter(status=0).all()
        if 'search' in self.request.GET:
            search = self.request.GET.get('search')
            articles = articles.filter(
                Q(title__icontains=search) |
                Q(summary__icontains=search) |
                Q(tags__icontains=search)
            )
        f = ArticleFilter(self.request.GET, queryset=articles)
        return f.qs.order_by('-is_top', '-publish_time')

    def get_context_data(self, **kwargs):
        kwargs['column'] = self.get_object()
        return super(ColumnView, self).get_context_data(**kwargs)

    def get_queryset(self):
        articles = self.get_articles()
        article_list = self.get_object().article.filter(id__in=[x.id for x in articles]).all()
        return article_list

