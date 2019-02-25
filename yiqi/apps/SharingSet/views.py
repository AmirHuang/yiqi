from rest_framework import mixins, viewsets, views, status
from rest_framework.response import Response
from rest_framework import authentication  # 身份验证
from utils.permissions import IsOwnerOrReadOnly  # 登陆验证
from rest_framework.permissions import IsAuthenticated  # 验证登陆
from rest_framework_jwt.authentication import JSONWebTokenAuthentication  # 身份验证

from SharingSet.models import SharingSetModel
from SharingSet.serializers import SharingSerializers


class SharingViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    # 获取全部分享设置的数据
    SET_PATH = ''

    def get_queryset(self):
        queryset = SharingSetModel.objects.filter(set_path=self.SET_PATH)
        return queryset
    serializer_class = SharingSerializers


class GeneralSharingViewSet(SharingViewset):
    # 获取通用分享数据
    SET_PATH = '0'


class ActivitySharingViewSet(SharingViewset):
    # 获取活动页面分享数据
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    SET_PATH = '1'


class ReleaseSharingViewSet(SharingViewset):
    '''
    获取发布页面分享数据
    '''
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    SET_PATH = '2'


class FoundSharingViewSet(SharingViewset):
    '''
    获取发现页面分享数据
    '''
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    SET_PATH = '3'


class MessagesSharingViewSet(SharingViewset):
    '''
    获取消息页面分享数据
    '''
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    SET_PATH = '4'


class ContentSharingViewSet(SharingViewset):
    '''
    获取内容页面分享数据
    '''
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    SET_PATH = '5'
