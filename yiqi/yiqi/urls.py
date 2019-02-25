"""yiqi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
from django.urls import path, include, re_path
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from yiqi.settings import MEDIA_ROOT, STATIC_ROOT
from activity.views import ActivityTypeView, UploadTextDateView, ActivityModelViewset
from activity.views import SlideIndexViewset, SearchAllDateViewset
from activity.views import MapModelAllDateViewSet, StartAllDataViewSet, RegistrationAllDataViewSet
from messagess.views import SysMessagesViewSet, UserMessageListViewSet, UserMessageViewSet
from SharingSet.views import GeneralSharingViewSet, ActivitySharingViewSet
from userOperation.views import SharingUserViewSet, SharingUserModelViewset, BrowseUserViewSet, BrowseUserViewset
from userOperation.views import ActivityUserInfoViewset, CollectionUserModelViewset
from userOperation.views import ReporttionUserModelViewset, RegisteredUserViewSet, RegisteredUserViewset
from userOperation.views import UserAllActivityView, UserbrowseView, ActivityUserinfoView
from userOperation.views import FeedBackViewSet, CommentsModelsUserViewset, CommentsModelsUserViewSet
router = DefaultRouter()

# 评论
router.register(r'comments', CommentsModelsUserViewset, base_name='comments')

# 反馈
router.register(r'FeedBackViewSet', FeedBackViewSet, base_name='FeedBackViewSet')

# 获取当前用户发布的所有信息
router.register(r'UserAllActivityView', UserAllActivityView, base_name='UserAllActivityView')

# 获取当前用户浏览的所有信息
router.register(r'UserbrowseView', UserbrowseView, base_name='UserbrowseView')

# 获取参加者的报名信息
router.register(r'ActivityUserinfoView', ActivityUserinfoView, base_name='ActivityUserinfoView')

# 活动类型
router.register(r'activitytype', ActivityTypeView, base_name='activitytype')

# 活动
router.register(r'activity', ActivityModelViewset, base_name='activity')

# 首页幻灯片
router.register(r'slide', SlideIndexViewset, base_name='slide')

# 数据搜索
router.register(r'searchalldate', SearchAllDateViewset, base_name='searchalldate')

# 地图数据
router.register(r'map', MapModelAllDateViewSet, base_name='map')

# 获取即将开始的数据
router.register(r'startalldata', StartAllDataViewSet, base_name='startalldata')

# 获取热门数据
router.register(r'hot', RegistrationAllDataViewSet, base_name='hot')

# 获取系统消息列表
router.register(r'sysmessagelist', SysMessagesViewSet, base_name='sysmessagelist')

# 获取系统消息列表
router.register(r'sysmessage', UserMessageViewSet, base_name='sysmessage')

# 获取通用分享数据
router.register(r'generalshare', GeneralSharingViewSet, base_name='generalshare')

# 获取活动页面分享数据
router.register(r'activityshare', ActivitySharingViewSet, base_name='activityshare')

# 用户分享接口
router.register(r'shareuser', SharingUserModelViewset, base_name='shareuser')

# 获取用户浏览记录
router.register(r'browseruser', BrowseUserViewset, base_name='browseruser')

# 保存报名信息
router.register(r'activityuserinfo', ActivityUserInfoViewset, base_name='activityuserinfo')

# 收藏 取消收藏
router.register(r'collection', CollectionUserModelViewset, base_name='collection')

# 举报
router.register(r'report', ReporttionUserModelViewset, base_name='report')

# 获取当前报名的用户信息
router.register(r'register', RegisteredUserViewset, base_name='register')


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('ueditor/', include('DjangoUeditor.urls')),

    # 文件
    path('upload/<path:path>', serve, {'document_root': MEDIA_ROOT}),
    path('static/<path:path>', serve, {'document_root': STATIC_ROOT}),

    # drf 文档
    path('docs', include_docs_urls(title='Amir')),
    path('api-auth/', include('rest_framework.urls')),

    re_path(r'', include(router.urls)),
    re_path(r'^UploadTextDateView/$', UploadTextDateView.as_view(), name='UploadTextDateView'),  # 保存活动数据
    re_path(r'UserMessageListViewSet/$', UserMessageListViewSet.as_view(), name='UserMessageListViewSet'),

    re_path(r'SharingUserViewSet/$', SharingUserViewSet.as_view(), name='SharingUserViewSet'),
    re_path(r'BrowseUserViewSet/$', BrowseUserViewSet.as_view(), name='BrowseUserViewSet'),  # 保存浏览用户
    # 获取当前报名的用户信息
    re_path(r'RegisteredUserViewSet/$', RegisteredUserViewSet.as_view(), name='RegisteredUserViewSet'),  # 保存浏览用户
    re_path(r'CommentsModelsUserViewSet/$', CommentsModelsUserViewSet.as_view(), name='CommentsModelsUserViewSet'),

]
