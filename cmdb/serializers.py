# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : serializers.py
# Time       ：2022/3/24 9:33
# Author     ：Andy
"""

from .models import Host, CloudHost
from rest_framework import serializers


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = '__all__'


class CloudHostSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        cloud_hosts = CloudHost.objects.update_or_create(
            instance_id=validated_data.get('instance_id', None),
            defaults=validated_data)
        return cloud_hosts

    class Meta:
        model = CloudHost
        fields = '__all__'
