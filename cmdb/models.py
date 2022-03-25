from django.db import models
from django.db.models import JSONField

import uuid


class Host(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    hostname = models.CharField(max_length=30, verbose_name="主机名")
    instance_id = models.CharField(max_length=30, null=True, verbose_name="云主机实例 id")
    cloud_info = models.ForeignKey('CloudHost', on_delete=models.CASCADE, null=True, verbose_name="云主机信息")


class CloudHost(models.Model):
    instance_id = models.CharField(max_length=30, verbose_name="实例 id")
    instance_type = models.CharField(max_length=30, null=True, verbose_name="实例规格")
    instance_type_family = models.CharField(max_length=20, null=True, verbose_name="实例规格组")
    image_id = models.CharField(max_length=60, null=True, verbose_name="实例镜像")
    resource_group_id = models.CharField(max_length=30, null=True, verbose_name="资源组")
    public_ip_address = JSONField(null=True, verbose_name="公网 ip")
    region_id = models.CharField(max_length=20, null=True, verbose_name="地域 id")
    zone_id = models.CharField(max_length=20, null=True, verbose_name="可用区 id")
    instance_charge_type = models.CharField(max_length=20, null=True, verbose_name="实例计费方式")
    internet_charge_type = models.CharField(max_length=20, null=True, blank=True, verbose_name="公网带宽计费方式")
    creation_time = models.DateTimeField(null=True, verbose_name="创建时间")
    expired_time = models.DateTimeField(null=True, verbose_name="过期时间")


