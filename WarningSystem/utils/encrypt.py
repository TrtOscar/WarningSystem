"""
md5加密
"""

from django.conf import settings
import hashlib


def md5(data_string):
    # 创建md5对象
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    # 加密
    obj.update(data_string.encode('utf-8'))
    # 返回加密结果
    return obj.hexdigest()
