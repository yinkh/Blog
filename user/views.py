import json
import base64
from PIL import Image

from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth import logout
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.mixins import LoginRequiredMixin
from common.views import BaseContextMixin
from notification.models import Notification
from .forms import *
from .utils import *

logger = logging.getLogger(__name__)


# 登陆
class LoginView(BaseContextMixin, FormView):
    template_name = 'user/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        # 发送激活验证邮件
        if 'active_email' in self.request.GET:
            active_email = self.request.GET.get('active_email')
            try:
                user = User.objects.get(email=active_email, email_active=False)
                kwargs['message'] = send_active_email(self.request, user)
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                kwargs['message'] = '邮箱不存在或账户已激活'
        # 激活账户
        if 'active_code' in self.request.GET:
            active_code = self.request.GET.get('active_code')
            try:
                email_verify = EmailVerify.objects.get(verify_code=active_code, category=0)
                email_verify.owner.email_active = True
                email_verify.owner.save()
                email_verify.delete()
                kwargs['message'] = '邮箱{}已激活'.format(email_verify.owner.email)
            except ObjectDoesNotExist:
                kwargs['message'] = '该链接已失效'
            except MultipleObjectsReturned:
                EmailVerify.objects.filter(verify_code=active_code, category=0).delete()
                kwargs['message'] = '发生错误,请重新请求激活邮件!'
        return super(LoginView, self).get_context_data(**kwargs)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(request=self.request, **self.get_form_kwargs())


# 登出
class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated():
            logout(request)
        return HttpResponseRedirect(reverse_lazy('index'))


# 注册
class RegisterView(BaseContextMixin, FormView):
    template_name = 'user/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('user_login')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())


# 找回密码
class ForgetPasswordView(BaseContextMixin, FormView):
    template_name = 'user/forget_password.html'
    form_class = ForgetPasswordForm

    def form_valid(self, form):
        form.save(request=self.request)
        # 不可直接redirect,必须将该form(带有message用于提示并判断是否跳转至登陆界面)直接返回
        return self.render_to_response(self.get_context_data(form=form))


# 找回密码-输入新密码
class ResetPasswordView(View):
    @staticmethod
    def get_email_verify(random):
        try:
            email_verify = EmailVerify.objects.get(verify_code=random, category=1)
        except ObjectDoesNotExist:
            email_verify = None
        except MultipleObjectsReturned:
            email_verify = None
            EmailVerify.objects.filter(verify_code=random, category=1).delete()
        return email_verify

    def get(self, request, random):
        email_verify = self.get_email_verify(random)
        user = email_verify.owner if email_verify else None
        form = SetPasswordForm(user)
        return render(request, 'user/reset_password.html', {'form': form})

    def post(self, request, random):
        email_verify = self.get_email_verify(random)
        user = email_verify.owner if email_verify else None
        form = SetPasswordForm(user, request.POST)
        if user and form.is_valid():
            form.save()
            email_verify.delete()
        return render(request, 'user/reset_password.html', {'form': form})


# 修改密码
class ChangePasswordView(BaseContextMixin, LoginRequiredMixin, FormView):
    template_name = 'user/change_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('user_change_pwd')

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(user=self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        # 不可直接redirect,必须将该form(带有message用于提示并判断是否跳转至登陆界面)直接返回
        return self.render_to_response(self.get_context_data(form=form))


# 修改头像
class ChangePortraitView(LoginRequiredMixin, BaseContextMixin, TemplateView):
    template_name = 'user/change_portrait.html'

    def post(self, request):
        data = request.POST['tx']
        if not data:
            return HttpResponse(u"请裁剪头像", status=500)
        img_base64 = base64.b64decode(data)
        file_dir = "user/"
        media_root = getattr(settings, 'MEDIA_ROOT', None)
        if media_root:
            file_dir = os.path.join(media_root, 'user/')
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        name = user_portrait_path(request.user, 'portal.png')
        path = os.path.join(media_root, name)

        file = open(path, "wb+")
        file.write(img_base64)
        file.flush()
        file.close()

        # 修改头像分辨率
        im = Image.open(path)
        out = im.resize((200, 200), Image.ANTIALIAS)
        out.save(path)

        # 选择上传头像到本地
        # 只需要为image存储文件名即可 url为base_url+user.image字段值
        request.user.portrait = name
        request.user.save()
        # 验证上传是否错误
        if not os.path.exists(path):
            return HttpResponse(u"上传头像错误", status=500)

        return HttpResponse(u"上传头像成功!")


# 消息通知
class NotificationView(LoginRequiredMixin, BaseContextMixin, TemplateView):
    template_name = 'user/notification.html'

    def get_context_data(self, **kwargs):
        kwargs['notifications'] = self.request.user.to_user_notification_set.order_by('-create_time').all()
        return super(NotificationView, self).get_context_data(**kwargs)

    def post(self, request):
        notification_id = self.request.POST.get("notification_id", "")
        notification_id = int(notification_id)

        notification = Notification.objects.filter(
            pk=notification_id
        ).first()

        if notification:
            notification.is_read = True
            notification.save()
            mydict = {"url": notification.url}
        else:
            mydict = {"url": '#'}

        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )
