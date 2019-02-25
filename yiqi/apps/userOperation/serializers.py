# _*_ coding: utf-8 _*_
# @Time     : 10:20
# @Author   : Amir
# @Site     : 
# @File     : serializers.py
# @Software : PyCharm

import datetime
from rest_framework import serializers

from activity.models import ActivityModel
from yiqi.settings import IMAGES_URL
from userOperation.models import ActivityUserInfo, CommentsModels, BrowseUserModel, CollectionUserModel
from rest_framework.validators import UniqueTogetherValidator
from .models import SharingUserModel, ReporttionUserModel
from users.serializers import UserDetailSerializer
from .models import FeedBackModels
now = datetime.datetime.now()
start = now - datetime.timedelta(hours=23, minutes=59, seconds=59)


class FeedBackModelsSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeedBackModels
        fields = '__all__'


class ActivityUserInfoSerializerstwo(serializers.ModelSerializer):

    def create(self, validated_data):
        activity = validated_data['activity']
        user = validated_data['user']
        activityuserinfo = ActivityUserInfo.objects.filter(user=user, activity=activity)
        if activityuserinfo:
            raise serializers.ValidationError('已报名')
        else:
            if int(activity.registration_number) >= int(activity.limitnum):
                raise serializers.ValidationError('报名人数已满')
            else:
                activityuserinfo = ActivityUserInfo.objects.create(**validated_data)
                # activity.registration_number += 1
                # activity.save()  # 再view里面写逻辑更合适把可能
                return activityuserinfo

    class Meta:
        model = ActivityUserInfo
        fields = '__all__'


class SharingUserModelSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SharingUserModel
        fields = '__all__'


class BrowseUserModelSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        user = validated_data['user']
        activity = validated_data['activity']
        exsted = BrowseUserModel.objects.filter(user=user, activity=activity)
        if exsted:
            exsted = exsted[0]
            exsted.addtime = datetime.datetime.now()
            exsted.save()
        else:
            exsted = BrowseUserModel.objects.create(**validated_data)
        return exsted

    class Meta:
        model = BrowseUserModel
        fields = '__all__'


class RegisteredUserSerializers(serializers.ModelSerializer):
    # 获取每个活动下面报名的用户, 如果当前查看的用户已经报名就显示用户名和微信号
    user = serializers.SerializerMethodField(read_only=True)  # 获取用户
    username = serializers.SerializerMethodField(read_only=True)  # 获取报名的用户名
    wechat = serializers.SerializerMethodField(read_only=True)  # 获取已经报名的用户微信
    type = serializers.SerializerMethodField(read_only=True)

    def get_type(self, obj):
        '''
        报名人员还是发起人员
        :param obj:
        :return:
        '''
        if obj.type == '0':
            return '活动发起人'
        else:
            return '活动参加人'

    def get_username(self, obj):
        '''
        获取用户报名的名字，如果访问的用户没有报名就不能显示
        :param obj:
        :return:
        '''
        print('----------------context', self.context)
        this_user = self.context['user']
        # 这里的id 是前端传进来的 如http://127.0.0.1:8000/RegisteredUserViewSet/?id=11
        # 这个id保存在context里面
        id = self.context['id']
        register = ActivityUserInfo.objects.filter(user=this_user, activity__id=id)
        if register:
            return obj.username
        else:
            return '仅限报名成员查看'

    def get_wechat(self, obj):
        '''
        获取用户报名的微信，如果访问的用户没有帮忙微信就不会显示
        :param obj:
        :return:
        '''
        this_user = self.context['user']
        id = self.context['id']
        register = ActivityUserInfo.objects.filter(user=this_user, activity__id=id)
        if register:
            return obj.wechat
        else:
            return '仅限报名成员查看'

    def get_user(self, obj):
        '''
        返回用户的头像和名称，性别
        :param obj:
        :return:
        '''
        if obj.user.thesignature:
            thesignature = obj.user.thesignature
        else:
            thesignature = '还没有设置签名。'
        return {'avatar': IMAGES_URL + 'upload/' + str(obj.user.avatar), 'name': obj.user.name,
                'gender': obj.user.gender, 'thesignature': thesignature}

    class Meta:
        model = ActivityUserInfo
        fields = '__all__'


class RegisteredUserSerializersTwo(serializers.ModelSerializer):
    # 获取每个活动下面报名的用户, 如果当前查看的用户已经报名就显示用户名和微信号
    user = serializers.SerializerMethodField(read_only=True)  # 获取用户
    username = serializers.SerializerMethodField(read_only=True)  # 获取报名的用户名
    wechat = serializers.SerializerMethodField(read_only=True)  # 获取已经报名的用户微信
    type = serializers.SerializerMethodField(read_only=True)

    def get_type(self, obj):
        '''
        报名人员还是发起人员
        :param obj:
        :return:
        '''
        if obj.type == '0':
            return '活动发起人'
        else:
            return '活动参加人'

    def get_username(self, obj):
        '''
        获取用户报名的名字，如果访问的用户没有报名就不能显示
        :param obj:
        :return:
        '''
        print('--------------self.context', self.context)
        this_user = self.context.get('request').user
        # 这里的id 是前端传进来的 如http://127.0.0.1:8000/RegisteredUserViewSet/?id=11
        # 这个id保存在context里面
        id = self.context.get('request').query_params.get('activity_id')
        register = ActivityUserInfo.objects.filter(user=this_user, activity__id=id)
        if register:
            return obj.username
        else:
            return '仅限报名成员查看'

    def get_wechat(self, obj):
        '''
        获取用户报名的微信，如果访问的用户没有帮忙微信就不会显示
        :param obj:
        :return:
        '''
        this_user = self.context['request'].user
        id = self.context.get('request').query_params.get('activity_id')
        register = ActivityUserInfo.objects.filter(user=this_user, activity__id=id)
        if register:
            return obj.wechat
        else:
            return '仅限报名成员查看'

    def get_user(self, obj):
        '''
        返回用户的头像和名称，性别
        :param obj:
        :return:
        '''
        if obj.user.thesignature:
            thesignature = obj.user.thesignature
        else:
            thesignature = '还没有设置签名。'
        return {'avatar': IMAGES_URL + 'upload/' + str(obj.user.avatar), 'name': obj.user.name,
                'gender': obj.user.gender, 'thesignature': thesignature}

    class Meta:
        model = ActivityUserInfo
        fields = '__all__'


class ActivityUserInfoserializer(serializers.ModelSerializer):
    # user = UserDetailSerializer(many=True)

    class Meta:
        model = ActivityUserInfo
        fields = '__all__'


class CommentSerializers0(serializers.ModelSerializer):
    # 获取当前活动的全部评论数据

    user = serializers.SerializerMethodField(read_only=True)

    def get_user(self, obj):
        '''
        返回用户的头像和名称，性别
        :param obj:
        :return:
        '''
        return {'avatar': IMAGES_URL + 'upload/' + str(obj.user.avatar), 'name': obj.user.name,
                'gender': obj.user.gender}

    class Meta:
        model = CommentsModels
        fields = '__all__'


class UserAllActivitySerializers(serializers.ModelSerializer):
    # 获取当前用户发布的活动
    judgeStartEnd = serializers.SerializerMethodField(read_only=True)

    def get_judgeStartEnd(self, obj):
        if obj.enddate >= start:
            return True
        else:
            return False

    class Meta:
        model = ActivityModel
        fields = '__all__'


class UserbrowseSerializers(serializers.ModelSerializer):
    '''
    获取当前用户的浏览记录
    '''
    activity = UserAllActivitySerializers()

    class Meta:
        model = BrowseUserModel
        fields = '__all__'


class CollectionUserSerializers(serializers.ModelSerializer):
    '''
    获取当前用户的收藏记录
    '''
    activity = UserAllActivitySerializers()

    class Meta:
        model = CollectionUserModel
        fields = '__all__'


class CollectionUserSerializersTwo(serializers.ModelSerializer):
    '''
    获取当前用户的收藏记录
    '''
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        # #validate实现唯一联合，一个商品只能收藏一次
        validators = [
            UniqueTogetherValidator(
                queryset=CollectionUserModel.objects.all(),
                fields=('user', 'activity'),
                message='已收藏'
            )
        ]
        model = CollectionUserModel
        fields = '__all__'


class ReporttionUserModelSerializers(serializers.ModelSerializer):
    # 用户举报
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        # validate 实现联合唯一， 一个商品只能收藏一次
        validators = [
            UniqueTogetherValidator(
                queryset=ReporttionUserModel.objects.all(),
                fields=('user', 'activity'),
                message='已举报'
            )
        ]
        model = ReporttionUserModel
        fields = '__all__'


class ActivityUserInfoSerializers(serializers.ModelSerializer):
    '''
    获取当前用户的报名记录
    '''
    activity = UserAllActivitySerializers()

    class Meta:
        model = ActivityUserInfo
        fields = '__all__'


class CommentSerializers(serializers.ModelSerializer):
    # 获取当前活动的全部评论数据
    user_id = serializers.SerializerMethodField(read_only=True)

    def get_user_id(self, obj):
        '''
        返回用户的头像和名称，性别
        :param obj:
        :return:
        '''
        return {'avatar': IMAGES_URL + 'upload/' + str(obj.user.avatar),
                'name': obj.user.username,
                'gender': obj.user.gender}

    class Meta:
        model = CommentsModels
        fields = '__all__'


class SharingUserModelViewset(serializers.ModelSerializer):

    class Meta:
        model = SharingUserModel
        fields = '__all__'
