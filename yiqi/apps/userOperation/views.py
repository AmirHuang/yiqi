import datetime

from rest_framework import mixins, viewsets, views, status
from rest_framework.response import Response
from rest_framework import authentication
from utils.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from yiqi.settings import IMAGES_URL
from users.models import UserProFile
from userOperation.models import SharingSetModel, SharingUserModel, BrowseUserModel
from userOperation.serializers import SharingUserModelSerializers, BrowseUserModelSerializers
from activity.models import ActivityModel
from .models import ActivityUserInfo, SysMessages, CollectionUserModel, ReporttionUserModel
from .serializers import ActivityUserInfoSerializerstwo, CollectionUserSerializersTwo
from .serializers import ReporttionUserModelSerializers, RegisteredUserSerializers, ActivityUserInfoserializer
from .serializers import RegisteredUserSerializersTwo
from messagess.models import SysUserModel
from .serializers import UserAllActivitySerializers, UserbrowseSerializers, ActivityUserInfoSerializers, \
    FeedBackModelsSerializer
from .models import FeedBackModels, CommentsModels
from .serializers import CommentSerializers


class SharingUserViewSet(views.APIView):
    '''
    获取分享的用户
    '''
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def post(self, request):
        user = SharingUserModel()
        user.user = self.request.user
        user.save()
        return Response({'messages': '分享成功'}, status=status.HTTP_200_OK)


class SharingUserModelViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = SharingUserModel.objects.all().order_by('-addtime')
    serializer_class = SharingUserModelSerializers
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)


class BrowseUserViewSet(views.APIView):
    '''
    获取用户浏览记录
    '''
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def post(self, request):
        activityid = request.data['activityid']
        activity = ActivityModel.objects.filter(id=int(activityid))
        BrowseUser = BrowseUserModel.objects.filter(activity=activity[0], user=self.request.user)
        if BrowseUser:
            # 如果浏览记录存在就更新时间
            BrowseUser = BrowseUser[0]
            BrowseUser.addtime = datetime.datetime.now()
            BrowseUser.save()
            return Response(status=status.HTTP_200_OK)
        elif activity:
            # 如果浏览记录不存在就新建浏览记录
            user = BrowseUserModel()
            user.user = self.request.user
            user.activity = activity[0]
            user.save()
        return Response(status=status.HTTP_200_OK)


class BrowseUserViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    获取用户浏览记录
    '''
    queryset = BrowseUserModel.objects.all().order_by('-addtime')
    serializer_class = BrowseUserModelSerializers
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)


class ActivityUserInfoViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    # 保存报名信息
    queryset = ActivityUserInfo.objects.all().order_by('-addtime')
    serializer_class = ActivityUserInfoSerializerstwo
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        activityuserinfo = serializer.save()
        activity = activityuserinfo.activity
        activity.registration_number += 1
        activity.save()

        # 给当前报名的人员发送报名成功系统通知，给当前发起活动的人发送加入通知
        # sysuser = 系统用户
        # user = 接收用户
        # ISOPEN = 是否已读
        # activity = 活动
        # titles = 消息标题
        # content = 消息内容

        sysuser = SysUserModel.objects.filter(types='0')
        if sysuser:
            sysmessage = SysMessages()
            sysmessage.sysuser = sysuser[0]
            sysmessage.user = self.request.user
            sysmessage.activity = activity
            sysmessage.titles = '加入活动成功通知！'
            sysmessage.content = '您已成功加入【{name}】发起的【{title}】活动，活动时间【{start}】开始，【{end}】结束，快去与活动成员联系吧，记得准时参加活动哦！'.format(
                name=activity.user.username, title=activity.title,
                start=datetime.datetime.strftime(activity.startdate, '%Y-%m-%d'),
                end=datetime.datetime.strftime(activity.enddate, '%Y-%m-%d')
            )
            sysmessage.save()

            # 给活动发起人发送消息通知
            sysmessage0 = SysMessages()
            sysmessage0.sysuser = sysuser[0]
            sysmessage0.user = activity.user
            sysmessage0.activity = activity
            sysmessage0.titles = '朋友【{name}】加入了您发起的活动！'.format(name=self.request.user.username)
            sysmessage0.content = '朋友【{name}】成功加入了您发起的活动，快去和他联系吧！'.format(name=self.request.user.username, )
            sysmessage0.save()


class CollectionUserModelViewset(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                                 viewsets.GenericViewSet):
    # 收藏，取消收藏功能
    serializer_class = CollectionUserSerializersTwo
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    lookup_field = 'activity_id'

    def get_queryset(self):
        return CollectionUserModel.objects.filter(user=self.request.user)


class ReporttionUserModelViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                                 mixins.DestroyModelMixin, viewsets.GenericViewSet):
    # 用户举报
    serializer_class = ReporttionUserModelSerializers
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    lookup_field = 'activity_id'

    def get_queryset(self):
        return ReporttionUserModel.objects.filter(user=self.request.user)


class RegisteredUserViewSet(views.APIView):
    '''
    获取当前报名的用户信息
    '''
    authentication_classes = (authentication.SessionAuthentication,
                              JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get(self, request, format=None):
        '''
        获取已经报名的用户，如果没有报名就不能看到已经报名用户的信息
        :param request:
        :param format:
        :return:
        '''
        try:
            id = request.GET.get('id')
            user = self.request.user
        except:
            id = None
        if id != None:
            registeredUser = ActivityUserInfo.objects.filter(activity__id=id)
            registeredUser_Serializers = RegisteredUserSerializers(registeredUser,
                                                                   many=True,
                                                                   context={
                                                                       'user': user,
                                                                       'id': id
                                                                   })
            return Response(registeredUser_Serializers.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class RegisteredUserViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    获取当前报名的用户信息
    '''
    queryset = ActivityUserInfo.objects.all().order_by('-addtime')
    authentication_classes = (authentication.SessionAuthentication,
                              JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # serializer_class = ActivityUserInfoserializer
    serializer_class = RegisteredUserSerializersTwo
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('activity_id',)


class UserAllActivityView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    # 获取当前用户发布的所有信息
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserAllActivitySerializers

    def get_queryset(self):
        return ActivityModel.objects.filter(user=self.request.user).order_by('-addtime')


class UserbrowseView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    获取当前用户浏览的所有信息
    '''
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        query = BrowseUserModel.objects.filter(user=self.request.user).order_by('-addtime')
        return query

    serializer_class = UserbrowseSerializers


class ActivityUserinfoView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    获取参加者的报名信息
    '''
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        query = ActivityUserInfo.objects.filter(user=self.request.user, type='1').order_by('-addtime')
        return query

    serializer_class = ActivityUserInfoSerializers


class FeedBackViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    # 用户反馈接口
    queryset = FeedBackModels.objects.all().order_by('-addtime')
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = FeedBackModelsSerializer


class CommentsModelsUserViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    # 获取当前活动的全部评论数据
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = CommentsModels.objects.all().order_by('-addtime')
    serializer_class = CommentSerializers
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('activity_id',)
    # lookup_field = 'activity_id'


class CommentsModelsUserViewSet(views.APIView):
    # 获取当前活动的全部评论数据
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get(self, request, format=None):
        '''
        获取评论数据
        :param request:
        :param format:
        :return:
        '''
        try:
            id = request.GET.get('id')
            user = self.request.user
        except:
            id = None
        if id != None:
            this_act_com = CommentsModels.objects.filter(activity__id=id)
            this_act_com_Serializers = CommentSerializers(this_act_com, many=True, context={'user': user, 'id': id})
            return Response(this_act_com_Serializers.data)

        return Response(status=status.HTTP_401_UNAUTHORIZED)
