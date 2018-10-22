from django.db import models
from django.conf import settings


# 通知
class Notification(models.Model):
    # 标题
    title = models.CharField(max_length=100,
                             verbose_name='标题')
    # 内容
    text = models.TextField(verbose_name='内容')
    # 链接
    url = models.CharField(max_length=200,
                           null=True,
                           blank=True,
                           verbose_name='链接')
    # 发送用户
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  null=True,
                                  blank=True,
                                  related_name='from_user_notification_set',
                                  on_delete=models.SET_NULL,
                                  verbose_name='发送者')
    # 接收用户
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='to_user_notification_set',
                                null=True,
                                on_delete=models.SET_NULL,
                                verbose_name='接收用户')
    type = models.CharField(max_length=20,
                            null=True,
                            blank=True,
                            verbose_name='类型')
    # 是否已读
    IS_READ = {
        0: '未读',
        1: '已读'
    }
    is_read = models.IntegerField(default=0,
                                  choices=IS_READ.items(),
                                  verbose_name='是否已读')
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True,
                                       verbose_name='创建时间')
    # 更新时间
    update_time = models.DateTimeField(auto_now=True,
                                       verbose_name='更新时间')

    class Meta:
        verbose_name = '通知'
        verbose_name_plural = '通知'
        ordering = ['-create_time']



