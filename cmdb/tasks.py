# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : tasks.py
# Time       ：2022/3/24 14:14
# Author     ：Andy
"""
from __future__ import absolute_import, unicode_literals
from cmdb.utils.alicloud.ecs_collection import EcsCollection
from celery import shared_task
from environs import Env


env = Env()
env.read_env()

access_key_id = env("ACCESS_KEY_ID")
access_key_secret = env("ACCESS_KEY_SECRET")


@shared_task()
def ali_cloud_info_collect():
    ecs_collection = EcsCollection(access_key_id, access_key_secret)
    ecs_collection.store_ecs_info()


if __name__ == '__main__':
    ali_cloud_info_collect()
