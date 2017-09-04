from django.db import models

from common.utils import get_time_filename


def carousel_img_path(instance, filename):
    return 'banner/{}'.format(get_time_filename(filename))


# 轮播图
class Banner(models.Model):
    # 标题
    title = models.CharField(max_length=100,
                             verbose_name=u'标题')
    # 摘要
    summary = models.TextField(null=True,
                               blank=True,
                               verbose_name=u'摘要')
    # 轮播图片
    img = models.FileField(upload_to=carousel_img_path,
                           verbose_name=u'轮播图片')
    # 手机轮播图片
    img_xs = models.FileField(upload_to=carousel_img_path,
                              verbose_name=u'手机轮播图片')
    # 文章
    article = models.ForeignKey('article.Article',
                                verbose_name=u'文章')
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True,
                                       verbose_name=u'创建时间')

    class Meta:
        verbose_name_plural = verbose_name = u'轮播图'
        ordering = ['-create_time']
