# _*_ coding: utf-8 _*_
# @Time     : 10:22
# @Author   : Amir
# @Site     : 
# @File     : serializers.py
# @Software : PyCharm

import datetime
from rest_framework import serializers

from yiqi.settings import IMAGES_URL
from userOperation.models import ReporttionUserModel, CollectionUserModel, ActivityUserInfo
from activity.models import ActivityTypeModel, ActivityModel, ActivityImagesModel, SlideModels

now = datetime.datetime.now()
start = now - datetime.timedelta(hours=23, minutes=59, seconds=59)


class ActivityTypeSerializers(serializers.ModelSerializer):

    class Meta:
        model = ActivityTypeModel
        fields = '__all__'


class ActivityImagesModelSerializers(serializers.ModelSerializer):
    # 获取活动图片
    class Meta:
        model = ActivityImagesModel
        fields = '__all__'


class ActivityDataSerializers(serializers.ModelSerializer):
    # 活动数据
    judgeStartEnd = serializers.SerializerMethodField(read_only=True)

    def get_judgeStartEnd(self, obj):
        if obj.enddate >= start:
            return True
        else:
            return False

    class Meta:
        model = ActivityModel
        fields = '__all__'


class ActivitySerializers(serializers.ModelSerializer):
    # activitytype = ActivityTypeSerializers(many=False)
    registration_number = serializers.IntegerField(read_only=True)
    audit = serializers.CharField(max_length=1, read_only=True)
    addtime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ActivityModel
        fields = '__all__'


class ActivityTypeDetailSerializers(serializers.ModelSerializer):
    # 分类数据的serializers
    activitytype = ActivityDataSerializers(many=True)

    class Meta:
        model = ActivityTypeModel
        fields = '__all__'


class SlideIndexSerializers(serializers.ModelSerializer):
    # 获取首页幻灯片数据

    class Meta:
        model = SlideModels
        fields = '__all__'


class SearchAllSerializers(serializers.ModelSerializer):
    # 搜索
    activitytype = serializers.SerializerMethodField(read_only=True)
    # enddate = serializers.DateTimeField(read_only=True, format=("%Y-%m-%d"))
    # startdate = serializers.DateTimeField(read_only=True, format=("%Y-%m-%d"))
    judgeStartEnd = serializers.SerializerMethodField(read_only=True)
    activi_info = serializers.SerializerMethodField(read_only=True)
    callections = serializers.SerializerMethodField(read_only=True)
    activi_number = serializers.SerializerMethodField(read_only=True)
    groupcode_is = serializers.SerializerMethodField(read_only=True)
    groupcode_none = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    wechat = serializers.SerializerMethodField(read_only=True)
    activity_images = ActivityImagesModelSerializers(many=True)
    groupcode = serializers.SerializerMethodField(read_only=True)

    def get_groupcode(self, obj):
        user = self.context['request'].user
        activi_info = ActivityUserInfo.objects.filter(activity=obj, user=user)
        if activi_info:
            if obj.groupcode:
                return IMAGES_URL + 'upload/' + str(obj.groupcode)
            else:
                return False
        else:
            return False

    def get_groupcode_none(self, obj):
        '''
        获取是否有上传群活动二维码
        :param obj:
        :return:
        '''
        if not str(obj.groupcode):
            return True
        else:
            return False

    def get_groupcode_is(self, obj):
        '''
        获取活动群二维码, false说明没有报名
        :param obj:
        :return:
        '''
        user = self.context['request'].user
        activi_info = ActivityUserInfo.objects.filter(activity=obj, user=user)
        if activi_info:
            return {'groupcode_is': True}
        else:
            return {'groupcode_is': False}

    def get_username(self, obj):
        '''
        如果用户已经报名就显示没有报名就不显示
        :param obj:
        :return:
        '''
        user = self.context['request'].user
        activi_info = ActivityUserInfo.objects.filter(activity=obj, user=user)
        if activi_info:
            return obj.username
        else:
            return '报名后可查看'

    def get_wechat(self, obj):
        '''
        如果用户已经报名就显示没有报名就不显示
        :param obj:
        :return:
        '''
        user = self.context['request'].user
        activi_info = ActivityUserInfo.objects.filter(activity=obj, user=user)
        if activi_info:
            return obj.wechat
        else:
            return '报名后可查看'

    def get_activi_info(self, obj):
        '''
        获取用户是否报名
        :param obj:
        :return:
        '''
        user = self.context['request'].user
        activi_info = ActivityUserInfo.objects.filter(activity=obj, user=user)
        if activi_info:
            return {'activi_info': True}
        else:
            return {'activi_info': False}

    def get_callections(self, obj):
        '''
        获取用户是否收藏
        :param obj:
        :return:
        '''
        user = self.context['request'].user
        callections = CollectionUserModel.objects.filter(activity=obj, user=user)
        if callections:
            return {'callections': True}
        else:
            return {'callections': False}

    def get_activi_number(self, obj):
        '''
        获取这个活动是否人数已满
        :param obj:
        :return:
        '''
        if obj.limitnum <= obj.registration_number:
            return {'activi_number': False}
        else:
            return {'activi_number': True}

    def get_judgeStartEnd(self, obj):
        if obj.enddate >= start:
            return True
        else:
            return False

    def get_activitytype(self, obj):
        return obj.activitytype.name

    class Meta:
        model = ActivityModel
        fields = '__all__'
