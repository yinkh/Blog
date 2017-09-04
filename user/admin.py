from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission, Group

from .models import *


# 用户
class MyUserAdmin(UserAdmin):
    list_display = ['id', 'username', 'get_full_name', 'tel', 'email', 'gender']
    fieldsets = (
        ('登陆信息', {'fields': ('username', 'password')}),
        ('用户信息', {'fields': ('name', 'portrait', 'gender', 'email', 'email_active',  'tel', 'qq',
                             'we_chat', 'contact_address', 'introduction')}),
        ('权限', {'fields': ('is_active', 'is_staff', 'is_superuser',
                           'groups', 'user_permissions')}),
        ('重要日期', {'fields': ('last_login', 'date_joined')}),
    )
    ordering = ('id',)
    search_fields = ('username', 'name', 'tel', 'email')
admin.site.register(User, MyUserAdmin)


# 权限
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'content_type', 'codename']
    search_fields = ('name',)
admin.site.register(Permission, PermissionAdmin)


# 邮箱验证码
class EmailVerifyAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'category', 'verify_code']
admin.site.register(EmailVerify, EmailVerifyAdmin)


# 职务
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ('name',)
    filter_horizontal = ('permissions', )
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)