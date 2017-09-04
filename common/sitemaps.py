from django.contrib.sitemaps import Sitemap
from django.urls import reverse_lazy

from article.models import Article
from news.models import News
from column.models import Column


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['index', 'article_index', 'article_all', 'news_index', 'user_login', 'user_register',
                'user_forget_pwd', 'version', 'rss']

    def location(self, item):
        return reverse_lazy(item)


class ArticleSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return Article.objects.filter(is_public=True).all().order_by('-id')

    def location(self, item):
        return reverse_lazy('article_detail', kwargs={'pk': item.id})


class NewsSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return News.objects.all().order_by('-id')

    def location(self, item):
        return reverse_lazy('news_detail', kwargs={'pk': item.id})


class ColumnSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return Column.objects.all().order_by('-id')

    def location(self, item):
        return reverse_lazy('column_detail', kwargs={'pk': item.id})


sitemaps = {
    'static': StaticViewSitemap,
    'article': ArticleSitemap,
    'news': NewsSitemap,
    'column': ColumnSitemap,
}
