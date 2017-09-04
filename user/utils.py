from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site

from .models import EmailVerify


def send_active_email(request, user):
    current_site = get_current_site(request)
    site_name = current_site.name

    if EmailVerify.objects.filter(owner=user, category=0).exists():
        verify = EmailVerify.objects.filter(owner=user, category=0).first()
    else:
        verify = EmailVerify.objects.create(owner=user, category=0)
    verify.update()
    title = u"{} 激活账户".format(site_name)
    message = "".join([
        u"你收到这封邮件是因为你请求激活你在网站 {} 上的账户\n\n".format(site_name),
        u"访问该界面即可激活账户:\n\n",
        "{}\n\n".format(verify.get_active_email_url(request=request)),
        u"你的用户名为:  {}\n\n".format(user.username),
        u"感谢使用我们的站点!\n\n",
        u"{} 团队\n\n\n".format(site_name)
    ])

    try:
        send_mail(title, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        message = "账号激活邮件已发送,如果你没有收到邮件," \
                  " 请确保您所输入的邮箱地址是正确的, 并检查您的垃圾邮件文件夹。"
    except ConnectionRefusedError as e:
        message = e.strerror
    except Exception as e:
        message = str(e)
    return message
