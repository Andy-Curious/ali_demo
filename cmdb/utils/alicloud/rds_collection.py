# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : rds_collection.py
# Time       ：2022/3/23 10:16
# Author     ：Andy
"""

from pprint import pprint
from alibabacloud_rds20140815.client import Client as Rds20140815Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_rds20140815 import models as rds_20140815_models


def create_client(access_key_id, access_key_secret, endpoint='rds.aliyuncs.com'):
    config = open_api_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint=endpoint
    )
    # 访问的域名
    return Rds20140815Client(config)


def get_rds_regions(ali_client):
    describe_regions_request = rds_20140815_models.DescribeRegionsRequest()
    resp = ali_client.describe_regions(describe_regions_request)
    ali_regions = resp.body.regions.rdsregion
    ali_region_id_set = set()
    for ali_region in ali_regions:
        ali_region_id_set.add(ali_region.region_id)
    return ali_region_id_set


def get_region_rds(ali_client, ali_region_id):
    page_number = 1
    db_instances_l = []
    while True:
        describe_db_request = rds_20140815_models.DescribeDBInstancesRequest(
            region_id=ali_region_id,
            page_number=page_number,
            page_size=100  # 默认最多 100
        )
        resp = ali_client.describe_dbinstances(describe_db_request)
        db_instances = resp.body.items.dbinstance
        if len(db_instances):
            for db_instance in db_instances:
                db_instances_l.append(db_instance)
            page_number += 1
        else:
            return db_instances_l


if __name__ == '__main__':

    # 认证信息
    accessKey_id = 'LTAI5tLBwQfqexzQpdBVrbgW'
    accessKey_secret = 'Az1VubAnsO0wMuN7aUVUNz912gNDAV'

    client = create_client(accessKey_id, accessKey_secret)
    region_id_set = get_rds_regions(client)

    all_region_rds_l = []

    for region_id in region_id_set:
        print(region_id)
        region_rds_l = get_region_rds(client, region_id)
        all_region_rds_l += region_rds_l

    # pprint(all_region_rds_l)

    for rds in all_region_rds_l:
        print(rds.dbinstance_description)

    print(len(all_region_rds_l))
