from django.conf import settings
from django.urls import reverse_lazy
from django.utils.feedgenerator import Rss201rev2Feed
from django.contrib.syndication.views import Feed

from common.utils import get_value

from article.models import Article


class BlogFeed(Feed):
    feed_type = Rss201rev2Feed
    link = reverse_lazy('index')
    feed_url = reverse_lazy('rss')

    def title(self):
        return get_value(settings.WEBSITE_TITLE)

    def description(self):
        return get_value(settings.WEBSITE_SEO_DESCRIPTION)

    def items(self):
        return Article.objects.order_by('-pk')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.summary

    def item_link(self, item):
        return reverse_lazy('article_detail', kwargs={'pk': item.id})

    def feed_copyright(self):
        return "Copyright &copy; 2015-2017 " + get_value(settings.WEBSITE_TITLE)


