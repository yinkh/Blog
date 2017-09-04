from django.db import models


# 导航条
class NavBar(models.Model):
    # 名称
    name = models.CharField(max_length=40,
                            verbose_name=u'名称')
    # 指向地址
    url = models.CharField(max_length=200,
                           verbose_name=u'指向地址')
    # 排序(越大的越靠后)
    order = models.PositiveIntegerField(default=0,
                                        verbose_name=u'排序(越大的越靠后)')
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True,
                                       verbose_name=u'创建时间')

    class Meta:
        verbose_name_plural = '导航条'
        verbose_name = '导航条'
        ordering = ['order']

    def __str__(self):
        return self.name
