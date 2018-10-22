import os
import binascii
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from common.utils import get_time_filename, validate_attachment_size, sizeof_fmt


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
        verbose_name='用户名'
    )
    # 头像
    portrait = models.ImageField(upload_to=user_portrait_path,
                                 null=True,
                                 blank=True,
                                 verbose_name='头像')
    # 性别 必选
    GENDER = {
        0: '女',
        1: '男',
        2: '保密',
    }
    gender = models.IntegerField(choices=GENDER.items(),
                                 default=2,
                                 blank=True,
                                 verbose_name='性别')
    # 姓名
    name = models.CharField(max_length=30,
                            blank=True,
                            verbose_name='姓名')
    # 电子邮件
    email = models.EmailField(max_length=255,
                              unique=True,
                              null=True,
                              blank=True,
                              error_messages={
                                  'unique': "具有该电子邮件的用户已存在",
                              },
                              verbose_name='电子邮件')
    # 电子邮箱激活
    email_active = models.BooleanField(default=False,
                                       verbose_name='电子邮箱激活')
    # 手机号码
    tel = models.CharField(max_length=20,
                           unique=True,
                           null=True,
                           blank=True,
                           error_messages={
                               'unique': "具有该手机号码的用户已存在",
                           },
                           verbose_name='手机号码')
    # QQ
    qq = models.CharField(max_length=20,
                          null=True,
                          blank=True,
                          verbose_name='QQ')
    # 微信
    we_chat = models.CharField(max_length=40,
                               null=True,
                               blank=True,
                               verbose_name='微信')
    # 联系地址
    contact_address = models.CharField(max_length=255,
                                       null=True,
                                       blank=True,
                                       verbose_name='联系地址')
    # 简介
    introduction = models.TextField(max_length=200,
                                    blank=True,
                                    null=True,
                                    verbose_name='简介')
    # 控制该用户是否可以登录admin site
    is_staff = models.BooleanField(default=False,
                                   verbose_name='职员状态')
    # 反选既等同于删除用户
    is_active = models.BooleanField(default=True,
                                    verbose_name='是否激活')
    # 账号创建时间
    date_joined = models.DateTimeField(blank=True,
                                       default=timezone.now,
                                       verbose_name='账号创建日期')

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
        0: '账户激活',
        1: '找回密码',
    }
    category = models.IntegerField(choices=CATEGORY.items(),
                                   default=0,
                                   verbose_name='类型')
    # 验证码
    verify_code = models.CharField(max_length=254,
                                   null=True,
                                   verbose_name='验证码')

    def update(self):
        self.verify_code = self.generate_key()
        self.save()
        return self.verify_code

    def get_active_email_url(self, request):
        url = '{}?active_code={}'.format(request.build_absolute_uri(reverse('user_login', args=())), self.verify_code)
        return url

    def get_reset_pwd_url(self, request):
        return request.build_absolute_uri(reverse('user_reset_pwd', args=(self.verify_code,)))

    @staticmethod
    def generate_key():
        return binascii.hexlify(os.urandom(20)).decode()

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = '邮箱验证码'


def attachment_file(instance, filename):
    return 'attachment/{}'.format(get_time_filename(filename))


# 附件
class Attachment(models.Model):
    # 名称
    name = models.CharField(max_length=100,
                            verbose_name='名称')
    # 文件
    file = models.FileField(upload_to=attachment_file,
                            null=True,
                            validators=[validate_attachment_size],
                            verbose_name='文件')
    # filename
    filename = models.CharField(max_length=255,
                                blank=True,
                                verbose_name='文件名称')
    # 文件格式
    ext = models.CharField(max_length=255,
                           blank=True,
                           verbose_name='文件格式')
    # 文件大小
    size = models.CharField(max_length=255,
                            blank=True,
                            verbose_name='文件大小')
    # 下载次数
    download_times = models.IntegerField(default=0,
                                         verbose_name='下载次数')
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True,
                                       verbose_name='创建时间')
    # 更新时间
    update_time = models.DateTimeField(auto_now=True,
                                       verbose_name='更新时间')

    class Meta:
        verbose_name = '附件'
        verbose_name_plural = '附件'

    def save(self, *args, **kwargs):
        if not self.id:
            self.set_info()
        else:
            # 改
            this = Attachment.objects.get(id=self.id)
            if this.file != self.file:
                this.file.delete(save=False)
                self.set_info()
        return super(Attachment, self).save(*args, **kwargs)

    def set_info(self):
        filename = self.file.name
        self.filename = filename
        ext = os.path.splitext(filename)[1][1:]
        self.ext = ext
        self.size = sizeof_fmt(self.file.size)

    def __str__(self):
        return self.name
