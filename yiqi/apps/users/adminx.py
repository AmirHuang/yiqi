# _*_ coding: utf-8 _*_
# @Time     : 14:19
# @Author   : Amir
# @Site     : 
# @File     : adminx.py
# @Software : PyCharm


import xadmin

from users.models import UserProFile


class UserProFileAdmin(object):
    '''
    用户表显示
    '''
    list_display = ['id', "name", "nickName", "mobile", "gender", 'language', 'country',
                    'province',
                    'city']  # 后台显示类型
    search_fields = ["name", "nickName", "mobile", "gender", 'language', 'country', 'province',
                     'city']  # 设置搜索
    list_filter = ["name", "nickName", "mobile", "gender", 'language', 'country', 'province',
                   'city']  # 搜索过滤器


xadmin.site.unregister(UserProFile)
xadmin.site.register(UserProFile, UserProFileAdmin)  # 普通用户
