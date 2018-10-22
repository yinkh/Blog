from django.db import models


class Link(models.Model):
    # 名称
    name = models.CharField(max_length=100,
                            verbose_name='名称')
    # 链接
    url = models.URLField(max_length=200,
                          null=True,
                          verbose_name='链接')
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True,
                                       verbose_name='创建时间')
    # 更新时间
    update_time = models.DateTimeField(auto_now=True,
                                       verbose_name='更新时间')

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = '友情链接'
        ordering = ['-create_time']
