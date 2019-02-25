# _*_ coding: utf-8 _*_
# @Time     : 15:56
# @Author   : Amir
# @Site     : 
# @File     : adminx.py
# @Software : PyCharm

import xadmin
from SharingSet.models import SharingSetModel


class SharingSetModelAdmin(object):
    list_display = ["set_path", "title", "addtime"]  # 后台显示类型
    search_fields = ["set_path", "title", "addtime"]  # 设置搜索
    list_filter = ["set_path", "title", "addtime"] # 搜索过滤器
    model_icon = "fa fa-share-alt"  # 这样可以替换与设置原有的Xadmin的图标


xadmin.site.register(SharingSetModel, SharingSetModelAdmin)

