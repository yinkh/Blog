from django.db import models
from django.utils import timezone
from django.conf import settings
from common.utils import get_time_filename


# 分类
class Category(models.Model):
    # 名称
    name = models.CharField(max_length=40,
                            verbose_name=u'名称')
    # 上级分类
    parent = models.ForeignKey('self',
                               default=None,
                               null=True,
                               blank=True,
                               verbose_name=u'上级分类')
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True,
                                       verbose_name=u'创建时间')
    # 更新时间
    update_time = models.DateTimeField(auto_now=True,
                                       verbose_name=u'更新时间')

    class Meta:
        verbose_name_plural = '分类'
        verbose_name = '分类'
        ordering = ['-create_time']

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('category-detail-view', args=(self.name,))

    def __str__(self):
        if self.parent:
            return '%s-->%s' % (self.parent, self.name)
        else:
            return '%s' % self.name


def article_img_path(instance, filename):
    return 'article/{}'.format(get_time_filename(filename))


# 公开文章Manager
class PublicManager(models.Manager):
    def get_queryset(self):
        return super(PublicManager, self).get_queryset().filter(is_public=True)


# 文章
class Article(models.Model):
    # 作者
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               null=True,
                               verbose_name=u'作者')
    # 分类
    category = models.ForeignKey(Category,
                                 verbose_name=u'分类')
    # 标题
    title = models.CharField(max_length=100,
                             verbose_name=u'标题')
    # 是否公开
    is_public = models.BooleanField(default=True,
                                    verbose_name=u'公开')
    # 展示图
    thumbnail = models.FileField(upload_to=article_img_path,
                                 null=True,
                                 blank=True,
                                 verbose_name=u'展示图')
    # 标签
    tags = models.CharField(max_length=200,
                            null=True,
                            blank=True,
                            verbose_name=u'标签',
                            help_text=u'用空格分隔')
    # 摘要
    summary = models.TextField(verbose_name=u'摘要')
    # 正文
    content = models.TextField(verbose_name=u'正文')
    # 查看次数
    view_times = models.IntegerField(default=0,
                                     verbose_name=u'查看次数')
    # 点赞次数
    zan_times = models.IntegerField(default=0,
                                    verbose_name='点赞次数')
    # 置顶
    is_top = models.BooleanField(default=False, verbose_name=u'置顶')
    # 状态 选项
    STATUS = {
        0: u'正常',
        1: u'草稿',
    }
    # 状态
    status = models.IntegerField(default=0,
                                 choices=STATUS.items(),
                                 verbose_name='状态')
    # 是否删除
    is_abandon = models.BooleanField(default=False,
                                     verbose_name=u'是否删除')
    # 发布时间
    publish_time = models.DateTimeField(default=timezone.now,
                                        verbose_name=u'发布时间')
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True,
                                       verbose_name=u'创建时间')
    # 更新时间
    update_time = models.DateTimeField(auto_now=True,
                                       verbose_name=u'更新时间')

    objects = models.Manager()
    public = PublicManager()

    def get_tags(self):
        tags_list = []
        if self.tags:
            tags_list = self.tags.split(' ')
            while '' in tags_list:
                tags_list.remove('')
        return tags_list

    class Meta:
        verbose_name_plural = '博客'
        verbose_name = '博客'
        ordering = ['-is_top', '-view_times', '-publish_time']

        permissions = (
            ("view_article", "查看所有文章"),
        )

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('article_detail', args=(self.id,))

    def __str__(self):
        return self.title


# 评论
class Comment(models.Model):
    # 用户
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=u'用户')
    # 文章
    article = models.ForeignKey('article.Article',
                                related_name='comment_article',
                                verbose_name=u'文章')
    # 评论内容
    text = models.TextField(verbose_name=u'评论内容')
    # 引用
    parent = models.ForeignKey('self',
                               null=True,
                               blank=True,
                               verbose_name=u'引用')
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True,
                                       verbose_name=u'创建时间')
    # 更新时间
    update_time = models.DateTimeField(auto_now=True,
                                       verbose_name=u'更新时间')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'

    def __str__(self):
        return '{}_{}'.format(self.article.title, self.pk)











