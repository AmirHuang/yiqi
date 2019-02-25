# _*_ coding: utf-8 _*_
# @Time     : 9:28
# @Author   : Amir
# @Site     : 
# @File     : serializers.py
# @Software : PyCharm

from rest_framework import serializers

from SharingSet.models import SharingSetModel


class SharingSerializers(serializers.ModelSerializer):
    # 获取分享数据
    class Meta:
        model = SharingSetModel
        fields = '__all__'