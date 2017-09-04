import os
import binascii
from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from common.utils import get_time_filename


def user_portrait_path(instance, filename):
    return 'user/{}'.format(get_time_filename(filename))


# 用户
class User(AbstractBaseUser, PermissionsMixin):
    # 用户名
    username = models.CharField(
        max_length=150,
        null=True,
        unique=True,
        help_text='用户名仅可包含字母、数字、-、_，但不可为纯数字。',
        validators=[RegexValidator(
            regex='^(?![0-9]*$)[-_\w]*$',
            message='用户名仅可包含字母、数字、-、_，但不可为纯数字。',
            code='invalid_username'
        )],
        error_messages={
            'unique': "该用户名已被注册",
        },
        verbose_name=u'用户名'
    )
    # 头像
    portrait = models.ImageField(upload_to=user_portrait_path,
                                 null=True,
                                 blank=True,
                                 verbose_name=u'头像')
    # 性别 必选
    GENDER = {
        0: u'女',
        1: u'男',
        2: u'保密',
    }
    gender = models.IntegerField(choices=GENDER.items(),
                                 default=2,
                                 blank=True,
                                 verbose_name=u'性别')
    # 姓名
    name = models.CharField(max_length=30,
                            blank=True,
                            verbose_name=u'姓名')
    # 电子邮件
    email = models.EmailField(max_length=255,
                              unique=True,
                              null=True,
                              blank=True,
                              error_messages={
                                  'unique': "具有该电子邮件的用户已存在",
                              },
                              verbose_name=u'电子邮件')
    # 电子邮箱激活
    email_active = models.BooleanField(default=False,
                                       verbose_name=u'电子邮箱激活')
    # 手机号码
    tel = models.CharField(max_length=20,
                           unique=True,
                           null=True,
                           blank=True,
                           error_messages={
                               'unique': "具有该手机号码的用户已存在",
                           },
                           verbose_name=u'手机号码')
    # QQ
    qq = models.CharField(max_length=20,
                          null=True,
                          blank=True,
                          verbose_name=u'QQ')
    # 微信
    we_chat = models.CharField(max_length=40,
                               null=True,
                               blank=True,
                               verbose_name=u'微信')
    # 联系地址
    contact_address = models.CharField(max_length=255,
                                       null=True,
                                       blank=True,
                                       verbose_name=u'联系地址')
    # 简介
    introduction = models.TextField(max_length=200,
                                    blank=True,
                                    null=True,
                                    verbose_name=u'简介')
    # 控制该用户是否可以登录admin site
    is_staff = models.BooleanField(default=False,
                                   verbose_name='职员状态')
    # 反选既等同于删除用户
    is_active = models.BooleanField(default=True,
                                    verbose_name=u'是否激活')
    # 账号创建时间
    date_joined = models.DateTimeField(blank=True,
                                       default=timezone.now,
                                       verbose_name=u'账号创建日期')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

        permissions = (
            ("view_cnzz", "查看站点流量"),
        )

    # 获取全名
    def get_full_name(self):
        if self.name == '':
            return self.username
        else:
            return self.name

    get_full_name.short_description = '全名'

    # 获取名称
    def get_short_name(self):
        return self.name

    # 向该用户发送邮件
    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_portrait(self):
        if self.portrait:
            return self.portrait.url
        else:
            return '/media/default/user/default.png'

    def __str__(self):
        return self.username


# 邮箱验证码
class EmailVerify(models.Model):
    # 用户
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              verbose_name='用户')
    # 类型
    CATEGORY = {
        0: u'账户激活',
        1: u'找回密码',
    }
    category = models.IntegerField(choices=CATEGORY.items(),
                                   default=0,
                                   verbose_name=u'类型')
    # 验证码
    verify_code = models.CharField(max_length=254,
                                   null=True,
                                   verbose_name='验证码')

    def update(self):
        self.verify_code = self.generate_key()
        self.save()
        return self.verify_code

    def get_active_email_url(self, request):
        from django.urls import reverse
        url = '{}?active_code={}'.format(request.build_absolute_uri(reverse('user_login', args=())), self.verify_code)
        print(url)
        return url

    def get_reset_pwd_url(self, request):
        from django.urls import reverse
        return request.build_absolute_uri(reverse('user_reset_pwd', args=(self.verify_code,)))

    @staticmethod
    def generate_key():
        return binascii.hexlify(os.urandom(20)).decode()

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = '邮箱验证码'
