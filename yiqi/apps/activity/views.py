import datetime
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, mixins, views
from rest_framework import authentication  # 身份验证
from rest_framework_jwt.authentication import JSONWebTokenAuthentication  # 身份验证
from rest_framework.permissions import IsAuthenticated  # 登陆验证
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from utils.permissions import IsOwnerOrReadOnly
from .models import ActivityTypeModel, ActivityModel, ActivityImagesModel, SlideModels
from .serializers import ActivityTypeDetailSerializers, ActivityTypeSerializers, ActivitySerializers
from .serializers import SlideIndexSerializers, SearchAllSerializers
from userOperation.models import ActivityUserInfo


class AllDynamicPagination(PageNumberPagination):
    '''
    自定义django_rest_fromework的页面参数
    '''
    page_size = 10  # 最少10条
    page_size_query_param = "page_size"  # 像后台声明要多少条
    page_query_param = "page"  # 要多少页
    max_page_size = 30  # 最多30条


class ActivityTypeView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    # 获取全部活动分类
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = ActivityTypeModel.objects.all().order_by('indexnum')
    serializer_class = ActivityTypeSerializers


class ActivityModelViewset(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = ActivityModel.objects.all().order_by('-addtime')
    serializer_class = ActivitySerializers

    def perform_create(self, serializer):
        activity = serializer.save()
        activityinfo = ActivityUserInfo.objects.create(user=activity.user,
                                                       type='0',
                                                       activity=activity,
                                                       username=activity.username,
                                                       wechat=activity.wechat)
        activityinfo.save()


class SlideIndexViewset(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = SlideModels.objects.all().order_by('indexnum')
    serializer_class = SlideIndexSerializers


class SearchAllDateViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    # 数据搜索
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = ActivityModel.objects.filter(audit='1', istrue=True, thedraft=True).order_by('-addtime')
    serializer_class = SearchAllSerializers
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("title", 'address', 'content', 'activitytype__name')
    ordering_fields = ("title", 'address', 'content', 'activitytype__name')
    pagination_class = AllDynamicPagination


class MapModelAllDateViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    # 地图数据
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = ActivityModel.objects.filter(audit='1', istrue=True, thedraft=True,
                                            startdate__gt=datetime.datetime.now()).order_by('-addtime')
    serializer_class = SearchAllSerializers


class StartAllDataViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    # 获取即将开始的数据
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    start = datetime.datetime.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
    queryset = ActivityModel.objects.filter(audit='1',
                                            istrue=True,
                                            thedraft=True,
                                            startdate__gt=datetime.datetime.now()).order_by('startdate')[:10]
    serializer_class = SearchAllSerializers
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)  # 精确过滤
    search_fields = ("title", 'address', 'content', 'activitytype__name')
    ordering_fields = ("title", 'address', 'content', 'activitytype__name')
    pagination_class = AllDynamicPagination  # 分页


class RegistrationAllDataViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    # 获取热门数据，这里按照报名人数进行排序只显示
    queryset = ActivityModel.objects.filter(audit='1',
                                            istrue=True,
                                            thedraft=True,
                                            enddate__gt=datetime.datetime.now()).order_by('-registration_number')
    serializer_class = SearchAllSerializers
    pagination_class = AllDynamicPagination
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)


class UploadTextDateView(views.APIView):
    '''
    发布活动
    '''
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def post(self, request):
        '''
        TEXT: 文本数据的保存，并且对数据进行安全效验
        BINARY: 二进制数据的保存，无需安全效验，需进行文件后缀效验
        :param request:
        :return:
        '''
        # print(request.FILES.get('file'))
        print(request.data['TYPE'])
        TYPE = request.data['TYPE']

        if TYPE == 'TEXT':
            user = self.request.user
            title = request.data['title']
            content = request.data['content']
            startdate = request.data['startdate']
            enddate = request.data['enddate']
            address = request.data['address']
            latitude = request.data['latitude']
            longitude = request.data['longitude']
            activitytype = request.data['activitytype']
            activitytype_id = request.data['activitytype_id']
            limitnum = request.data['limitnum']
            username = request.data['username']
            wechat = request.data['wechat']
            # 进行数据保存
            activiType = ActivityTypeModel.objects.filter(id=activitytype_id)
            if activiType:
                activi = ActivityModel()
                activi.user = user
                activi.title = title
                activi.content = content
                activi.startdate = startdate
                activi.enddate = enddate
                activi.address = address
                activi.latitude = latitude
                activi.longitude = longitude
                activi.activitytype = activiType[0]
                activi.limitnum = int(limitnum)
                activi.username = username
                activi.wechat = wechat
                activi.istrue = True
                activi.thedraft = True
                activi.registration_number = 1
                activi.save()

                # 把发起活动的人员设置到报名里面
                resing_user = ActivityUserInfo()
                resing_user.user = user
                resing_user.type = '0'
                resing_user.activity = activi
                resing_user.username = username
                resing_user.wechat = wechat
                resing_user.save()
                return Response({'id': activi.id}, status=status.HTTP_200_OK)
        elif TYPE == 'BINARY_FM':
            # 保存封面图片
            this_id = request.data['id']
            activi = ActivityModel.objects.filter(id=this_id)
            if activi:
                activi = activi[0]
                activi.cover_image = request.FILES.get('file')
                activi.save()
                return Response({'id': activi.id}, status=status.HTTP_200_OK)
        elif TYPE == 'BINARY_HD':
            # 保存活动图片
            this_id = request.data['id']
            len = request.data['len']
            activi = ActivityModel.objects.filter(id=this_id)
            if activi:
                activi = activi[0]
                activiType = ActivityImagesModel()
                activiType.activity = activi
                activiType.image = request.FILES.get('file')
                activiType.indexnum = int(len)
                activiType.save()
                return Response({'id': activi.id}, status=status.HTTP_200_OK)
        elif TYPE == 'BINARY_QR':
            # 保存群二维码图片
            this_id = request.data['id']
            activi = ActivityModel.objects.filter(id=this_id)
            if activi:
                activi = activi[0]
                activi.groupcode = request.FILES.get('file')
                activi.save()
                return Response({'id': activi.id}, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_401_UNAUTHORIZED)
