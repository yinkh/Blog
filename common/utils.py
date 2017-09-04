import os
from constance import LazyConfig
from datetime import datetime, timedelta

config = LazyConfig()


def put_value(key, value):
    """
    更新数据库设置项
    :param key: 键名
    :param value: 值
    :return: 无返回
    """
    setattr(config, key, value)


def get_value(key):
    """
    获取数据库设置项值
    :param key: 键名
    :return: 键名对应的设置项值
    """
    return getattr(config, key)


def get_time_filename(filename):
    """
    将文件名修改为 年月日-时分秒-毫秒 格式
    :param filename: 原文件名
    :return: 年月日-时分秒-毫秒
    """
    # 文件拓展名
    ext = os.path.splitext(filename)[1]
    # 文件目录
    d = os.path.dirname(filename)
    # 自定义文件名,年月日-时分秒-毫秒
    current_time = datetime.now().strftime('%Y%m%d-%H%M%S-%f')[:-3]
    # 合成文件名
    filename = os.path.join(d, current_time + ext)
    return filename


def get_ip(request):
    """
    :param request: request
    :return: ip地址
    """
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip
