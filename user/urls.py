from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='user_login'),
    url(r'^logout/$', LogoutView.as_view(), name='user_logout'),
    url(r'^register/$', RegisterView.as_view(), name='user_register'),
    url(r'^forget_pwd/$', ForgetPasswordView.as_view(), name='user_forget_pwd'),
    url(r'^reset_pwd/(?P<random>.+)/$', ResetPasswordView.as_view(), name='user_reset_pwd'),
    url(r'^change_pwd/$', ChangePasswordView.as_view(), name='user_change_pwd'),
    url(r'^portrait/$', ChangePortraitView.as_view(), name='user_portrait'),
    url(r'^notification/$', NotificationView.as_view(), name='user_notification'),
]
