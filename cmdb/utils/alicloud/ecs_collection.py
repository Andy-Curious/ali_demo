# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : ecs_collection.py
# Time       ：2022/3/23 10:16
# Author     ：Andy
"""

from alibabacloud_ecs20140526.client import Client as Ecs20140526Client
from alibabacloud_ecs20140526 import models as ecs_20140526_models
from alibabacloud_tea_openapi import models as open_api_models
from cmdb.serializers import CloudHostSerializer


class EcsCollection:

    """
    Collect Alibaba Cloud ECS information in batches
    """

    def __init__(self, access_key_id, access_key_secret):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret

    @staticmethod
    def create_client(access_key_id, access_key_secret, endpoint='ecs-cn-hangzhou.aliyuncs.com'):
        # TODO 偶尔超时
        config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            read_timeout=60000,
            connect_timeout=60000,
            protocol='HTTPS',
            endpoint=endpoint
        )
        return Ecs20140526Client(config)

    @staticmethod
    def get_ecs_regions(ali_client):
        describe_regions_request = ecs_20140526_models.DescribeRegionsRequest()
        resp = ali_client.describe_regions(describe_regions_request)
        ali_regions = resp.body.regions.region
        return ali_regions

    @staticmethod
    def get_region_ecs(ali_client, ali_region):
        page_number = 1
        instances_l = []
        while True:
            describe_instances_request = ecs_20140526_models.DescribeInstancesRequest(
                region_id=ali_region,
                page_number=page_number,
                page_size=100
            )
            resp = ali_client.describe_instances(describe_instances_request)
            instances = resp.body.instances.instance
            if len(instances):
                for instance in instances:
                    instances_l.append(instance)
                page_number += 1
            else:
                return instances_l

    def get_all_ecs(self):
        client = self.create_client(self.access_key_id, self.access_key_secret)
        region_l = self.get_ecs_regions(client)
        all_region_ecs_l = []

        for region in region_l:
            region_endpoint = region.region_endpoint
            region_id = region.region_id
            region_client = self.create_client(
                self.access_key_id, self.access_key_secret, region_endpoint)
            region_ecs_l = self.get_region_ecs(region_client, region_id)
            all_region_ecs_l += region_ecs_l

        return all_region_ecs_l

    def store_ecs_info(self):
        all_region_ecs_l = self.get_all_ecs()
        for ecs in all_region_ecs_l:
            ecs_info = ecs.__dict__
            ecs_info['public_ip_address'] = ecs.public_ip_address.__dict__
            serializer = CloudHostSerializer(data=ecs_info)
            if serializer.is_valid():
                serializer.save()


if __name__ == '__main__':
    pass
