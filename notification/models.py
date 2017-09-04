from django.db import models
from django.conf import settings


# 通知
class Notification(models.Model):
    # 标题
    title = models.CharField(max_length=100,
                             verbose_name=u'标题')
    # 内容
    text = models.TextField(verbose_name=u'内容')
    # 链接
    url = models.CharField(max_length=200,
                           null=True,
                           blank=True,
                           verbose_name=u'链接')
    # 发送用户
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  null=True,
                                  blank=True,
                                  related_name='from_user_notification_set',
                                  verbose_name=u'发送者')
    # 接收用户
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='to_user_notification_set',
                                verbose_name=u'接收用户')
    type = models.CharField(max_length=20,
                            null=True,
                            blank=True,
                            verbose_name=u'类型')
    # 是否已读
    IS_READ = {
        0: u'未读',
        1: u'已读'
    }
    is_read = models.IntegerField(default=0,
                                  choices=IS_READ.items(),
                                  verbose_name=u'是否已读')
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True,
                                       verbose_name=u'创建时间')
    # 更新时间
    update_time = models.DateTimeField(auto_now=True,
                                       verbose_name=u'更新时间')

    class Meta:
        verbose_name = u'通知'
        verbose_name_plural = u'通知'
        ordering = ['-create_time']



