from datetime import datetime
from django.db import models


# 新闻
class News(models.Model):
    # 标题
    title = models.CharField(max_length=100,
                             verbose_name=u'标题')
    # 摘要
    summary = models.TextField(verbose_name=u'摘要')
    # 来源
    source = models.CharField(max_length=100,
                              verbose_name='来源')
    # 源地址
    url = models.URLField(max_length=200,
                          verbose_name=u'源地址')
    # 发布时间
    publish_time = models.DateTimeField(default=datetime.now,
                                        verbose_name=u'发布时间')
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True,
                                       verbose_name=u'创建时间')
    # 更新时间
    update_time = models.DateTimeField(auto_now=True,
                                       verbose_name=u'更新时间')

    class Meta:
        verbose_name_plural = u'新闻'
        verbose_name = u'新闻'
        ordering = ['-id']

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('news-detail-view', args=(self.pk,))

    def __str__(self):
        return self.title
