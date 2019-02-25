# _*_ coding: utf-8 _*_
# @Time     : 15:45
# @Author   : Amir
# @Site     : 
# @File     : adminx.py
# @Software : PyCharm

import xadmin

from messagess.models import SysUserModel, SysUserthemenuModel


class SysUserModelAdmin(object):
    list_display = ["sysname", "sysIntroduction", "addtime"]  # 后台显示类型
    model_icon = "fa fa-commenting"  # 这样可以替换与设置原有的Xadmin的图标
    list_editable = ["sysname", "sysIntroduction"]  # 修改


class SysUserthemenuModelAdmin(object):
    list_display = ["sysuser", "themenu_name", "urls", "addtime"]  # 后台显示类型
    model_icon = "fa fa-commenting"  # 这样可以替换与设置原有的Xadmin的图标
    list_editable = ["sysuser", "themenu_name", "urls"]  # 修改


xadmin.site.register(SysUserModel, SysUserModelAdmin)
xadmin.site.register(SysUserthemenuModel, SysUserthemenuModelAdmin)
