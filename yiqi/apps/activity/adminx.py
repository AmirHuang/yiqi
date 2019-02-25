# _*_ coding: utf-8 _*_
# @Time     : 15:22
# @Author   : Amir
# @Site     : 
# @File     : adminx.py
# @Software : PyCharm

import xadmin
from xadmin import views
from activity.models import ActivityModel, ActivityImagesModel, ActivityTypeModel, SlideModels


class BaseSetting(object):
    # 添加主题功能
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    # 全局配置，后台管理标题和页脚
    site_title = "Amir"
    site_footer = "www.baidu.com"
    # 菜单收缩
    menu_style = "accordion"


class ActivityTypeModelAdmin(object):
    list_display = ["name", "Introduction", 'indexnum', "addtime"]  # 后台显示类型
    search_fields = ["name", "Introduction", 'indexnum', "addtime"]  # 设置搜索
    list_filter = ["name", "Introduction", 'indexnum', "addtime"]  # 搜索过滤器
    model_icon = "fa fa-refresh"  # 这样可以替换与设置原有的Xadmin的图标
    list_editable = ["indexnum", "Introduction"]  # 修改
    exclude = ('addtime',)


class ActivityImages(object):
    model = ActivityImagesModel
    extra = 0


class ActivityModelAdmin(object):
    list_display = ["user", "title", 'audit', 'content', "startdate", "enddate", "address", "latitude", "longitude",
                    "activitytype", "limitnum", "username", "wechat", "istrue", "thedraft", "addtime"]  # 后台显示类型
    search_fields = ["user", "title", 'audit', 'content', "startdate", "enddate", "address", "latitude", "longitude",
                     "activitytype", "limitnum", "username", "wechat", "istrue", "thedraft", "addtime"]  # 设置搜索
    list_filter = ["user", "title", 'audit', 'content', "startdate", "enddate", "address", "latitude", "longitude",
                   "activitytype", "limitnum", "username", "wechat", "istrue", "thedraft", "addtime"]  # 搜索过滤器
    model_icon = "fa fa-etsy"  # 这样可以替换与设置原有的Xadmin的图标
    list_editable = ["audit", "thedraft"]  # 修改
    exclude = ('addtime',)
    inlines = [ActivityImages, ]


class ActivityImagesModelAdmin(object):
    list_display = ["activity", "addtime"]  # 后台显示类型
    search_fields = ["activity", "addtime"]  # 设置搜索
    list_filter = ["activity", "addtime"]  # 搜索过滤器
    model_icon = "fa fa-camera"  # 这样可以替换与设置原有的Xadmin的图标
    exclude = ('addtime',)


class SlideModelsAdmin(object):
    list_display = ['activity', 'indexnum']
    search_fields = ['activity', 'indexnum']
    list_filter = ['activity', 'indexnum']
    model_icon = "fa fa-picture-o"
    list_editable = ["indexnum"]
    exclude = ('addtime',)


xadmin.site.register(ActivityTypeModel, ActivityTypeModelAdmin)
xadmin.site.register(ActivityModel, ActivityModelAdmin)
xadmin.site.register(ActivityImagesModel, ActivityImagesModelAdmin)
xadmin.site.register(SlideModels, SlideModelsAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
