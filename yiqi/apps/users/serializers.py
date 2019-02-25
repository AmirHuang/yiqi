# _*_ coding: utf-8 _*_
# @Time     : 17:46
# @Author   : Amir
# @Site     : 
# @File     : serializers.py
# @Software : PyCharm

from rest_framework import serializers

from users.models import UserProFile


class UserReSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProFile
        fields = ("name", "avatar", "gender", "password")


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProFile
        fields = ("username", "avatar", "gender")

