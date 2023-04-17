"""
    MD5加密

    data_string：需要加密的字符串

    在需要加密的属性中使用md5()
"""
import hashlib
from django.conf import settings


def md5(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))

    return obj.hexdigest()












