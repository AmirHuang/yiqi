from utils.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import mixins, viewsets
from rest_framework import authentication
from rest_framework import views
from rest_framework.response import Response

from yiqi.settings import IMAGES_URL
from userOperation.models import SysMessages
from messagess.models import SysUserthemenuModel, SysUserModel
from messagess.serializers import SysyUserSerializers, SysUserthemenuSerializers, SysuserMessagesSerializers


class SysMessagesViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    # 获取系统消息列表
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = SysUserModel.objects.all()
    serializer_class = SysyUserSerializers


class UserMessageListViewSet(views.APIView):
    '''
    获取系统消息内容
    '''
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get(self, request, format=None):
        id = request.GET['id']
        messageslist = SysMessages.objects.filter(user=self.request.user, sysuser__id=id)
        messageslist_serializers = SysuserMessagesSerializers(messageslist, many=True, context={'request': request})
        if messageslist:
            for msg in messageslist:
                msg.ISOPEN = '1'
                msg.save()
        return Response(messageslist_serializers.data)


class UserMessageViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    获取系统消息内容
    '''
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = SysMessages.objects.all().order_by('addtime')
    serializer_class = SysuserMessagesSerializers

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        messageslist = SysMessages.objects.filter(user=self.request.user, sysuser__id=instance.sysuser.id)
        if messageslist:
            for msg in messageslist:
                msg.ISOPEN = '1'
                msg.save()

        return Response(serializer.data)
