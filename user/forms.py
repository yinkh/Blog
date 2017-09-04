from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, login, password_validation
from django.contrib.sites.shortcuts import get_current_site

from .models import *
import logging

logger = logging.getLogger(__name__)


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['gender'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['tel'].widget.attrs.update({'class': 'form-control'})
        self.fields['qq'].widget.attrs.update({'class': 'form-control'})
        self.fields['we_chat'].widget.attrs.update({'class': 'form-control'})
        self.fields['contact_address'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = ['username', 'gender', 'name', 'email', 'tel',
                  'qq', 'we_chat', 'contact_address']


# 用户登陆Form
class LoginForm(forms.Form):
    active_email = None
    username = forms.CharField(label='用户名')
    password = forms.CharField(widget=forms.PasswordInput, label='密码')

    def __init__(self, request, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.request = request
        self.fields['username'].widget.attrs.update({'class': 'form-control',
                                                     "placeholder": self.fields['username'].label})
        self.fields['password'].widget.attrs.update({'class': 'form-control',
                                                     "placeholder": self.fields['password'].label})

    def clean(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.email_active:
                login(self.request, user)
            else:
                self.active_email = user.email
                self.add_error("username", "账户未激活")
        else:
            self.add_error("username", "账户名或密码输入错误")


# 参考自django.contrib.auth.forms.UserCreationForm
class UserCreationForm(forms.ModelForm):
    # 错误信息
    error_messages = {
        'duplicate_username': u"此用户已存在.",
        'password_mismatch': u"两次密码不相等.",
        'duplicate_email': u'此email已经存在.'
    }

    # 错误信息 invalid 表示username不合法的错误信息,
    # required 表示没填的错误信息
    username = forms.RegexField(
        max_length=30,
        regex=r'^[\w.@+-]+$',
        error_messages={
            'invalid': u"该值只能包含字母、数字和字符@/./+/-/_",
            'required': u"用户名未填"
        },
        label='用户名'
    )
    email = forms.EmailField(
        error_messages={
            'invalid': u"email格式错误",
            'required': u'email未填'},
        label='邮箱'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        error_messages={
            'required': u"密码未填"
        },
        label='密码'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        error_messages={
            'required': u"确认密码未填"
        },
        label='确认密码'
    )

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages["duplicate_username"]
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"]
            )
        password_validation.validate_password(password2)
        return password2

    def clean_email(self):
        email = self.cleaned_data["email"]

        # 判断是这个email 用户是否存在
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages["duplicate_email"]
        )

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ForgetPasswordForm(forms.Form):
    # 错误信息
    error_messages = {
        'email_error': "此用户不存在或者用户名与email不对应.",
    }
    email_send_message = None

    # 错误信息 invalid 表示username不合法的错误信息,
    # required 表示没填的错误信息
    username = forms.RegexField(
        max_length=30,
        regex=r'^[\w.@+-]+$',
        error_messages={
            'invalid': u"该值只能包含字母、数字和字符@/./+/-/_",
            'required': u"用户名未填"},
        label='用户名'
    )
    email = forms.EmailField(
        error_messages={
            'invalid': u"email格式错误",
            'required': u'email未填'},
        label='邮箱'
    )

    def __init__(self, *args, **kwargs):
        super(ForgetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if username and email:
            try:
                self.user = User.objects.get(username=username, email=email, is_active=True)
            except User.DoesNotExist:
                raise forms.ValidationError({'username': self.error_messages["email_error"]})
        return self.cleaned_data

    def save(self, request):
        current_site = get_current_site(request)
        site_name = current_site.name

        if EmailVerify.objects.filter(owner=self.user, category=1).exists():
            verify = EmailVerify.objects.filter(owner=self.user, category=1).first()
        else:
            verify = EmailVerify.objects.create(owner=self.user, category=1)
        verify.update()
        title = u"重置 {} 的密码".format(site_name)
        message = "".join([
            u"你收到这封邮件是因为你请求重置你在网站 {} 上的账户密码\n\n".format(site_name),
            u"请访问该页面并输入新密码:\n\n",
            "{}\n\n".format(verify.get_reset_pwd_url(request=request)),
            u"你的用户名为:  {}\n\n".format(self.user.username),
            u"感谢使用我们的站点!\n\n",
            u"{} 团队\n\n\n".format(site_name)
        ])

        try:
            send_mail(title, message, settings.DEFAULT_FROM_EMAIL, [self.user.email])
            self.email_send_message = "密码重置邮件已发送,如果你没有收到邮件," \
                                      " 请确保您所输入的地址是正确的, 并检查您的垃圾邮件文件夹。"
        except ConnectionRefusedError as e:
            self.add_error('email', e.strerror)
        except Exception as e:
            self.add_error('email', str(e))


class SetPasswordForm(forms.Form):
    error_messages = {
        'password_mismatch': "两次输入的密码不一致",
    }
    reset_pwd_message = None

    new_password1 = forms.CharField(
        label="新密码",
        widget=forms.PasswordInput,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="再次输入",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, user, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        password_validation.validate_password(password1, self.user)
        return password1

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        self.reset_pwd_message = '密码重置成功'
        return self.user


class PasswordChangeForm(forms.Form):
    error_messages = {
        'password_mismatch': "两次密码不相等",
        'password_incorrect': "旧密码输入错误",
    }
    message = None
    old_password = forms.CharField(
        label="请输入旧密码",
        strip=False,
        widget=forms.PasswordInput,
    )
    new_password1 = forms.CharField(
        label="请输入新密码",
        widget=forms.PasswordInput,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="请再次输入新密码",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, user, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'autofocus': True,
                                                         "placeholder": '旧密码'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control',
                                                          "placeholder": '新密码'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control',
                                                          "placeholder": '再次输入新密码'})

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect']
            )
        return old_password

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        self.message = '密码修改成功'
        return self.user
