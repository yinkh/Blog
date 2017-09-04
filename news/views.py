from datetime import timedelta

from django.views.generic import TemplateView, DetailView
from common.views import BaseContextMixin
from .models import *

# logger
import logging
logger = logging.getLogger("info")


class NewsView(BaseContextMixin, TemplateView):
    template_name = 'news/news.html'

    def get_context_data(self, **kwargs):
        timeblocks = []

        # 获取开始和终止的日期
        start_day = self.request.GET.get("start", "0")
        end_day = self.request.GET.get("end", "6")
        start_day = int(start_day)
        end_day = int(end_day)

        start_date = datetime.now()

        # 获取url中时间断的资讯
        for x in range(start_day, end_day + 1):
            date = start_date - timedelta(x)
            news_list = News.objects.filter(
                publish_time__year=date.year,
                publish_time__month=date.month,
                publish_time__day=date.day
            )
            if news_list:
                timeblocks.append(news_list)

        kwargs['timeblocks'] = timeblocks
        kwargs['active'] = start_day / 7  # li中那个显示active

        return super(NewsView, self).get_context_data(**kwargs)


class NewsDetailView(BaseContextMixin, DetailView):
    queryset = News.objects.all()
    slug_field = 'id'
    context_object_name = 'news'
    template_name = 'news/news_detail.html'
