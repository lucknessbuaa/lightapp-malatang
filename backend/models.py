# coding: utf-8

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class User(models.Model):
    AUTH_TYPES = (
        ('BAIDU', 'baidu'),
        ('WEIBO', 'weibo'),
        ('QQ', 'QQ'),
        ('WECHAT', 'WeChat'),
    )
    authType = models.CharField(verbose_name=u'类型', choices=AUTH_TYPES, default='QQ',max_length=16)
    authID = models.CharField(verbose_name=u'账号', max_length=255)
    authToken = models.CharField(verbose_name=u'验证', max_length=255)
        


class Dishes(models.Model):
    desc = models.TextField(verbose_name=u'介绍')
    cover = models.URLField(verbose_name=u'截图')
    name = models.CharField(verbose_name=u'名称', max_length=255)
    price = models.DecimalField(verbose_name=u'价格', max_digits=11, decimal_places=2)
    removed = models.BooleanField(default=False)


class Order(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(verbose_name=u'订餐时间',auto_now_add=True, blank=True)
    deadline = models.DateTimeField(verbose_name=u'送餐时间')
    complete = models.DateTimeField(verbose_name=u'送达时间')
    location = models.TextField(verbose_name=u'地点')
    contact = models.CharField(verbose_name=u'联系人',max_length=32)
    mobile = models.DecimalField(verbose_name=u'手机号',max_digits=11,decimal_places=0)
    number = models.SmallIntegerField(verbose_name=u'人数') # 餐具？
    total = models.DecimalField(verbose_name=u'总价', max_digits=11, decimal_places=2)
    count = models.IntegerField(verbose_name=u'份数')


class OrderItem(models.Model):
    price = models.DecimalField(verbose_name=u'合计', max_digits=11, decimal_places=2)
    count = models.IntegerField(verbose_name=u'份数')
    name = models.CharField(verbose_name=u'名称', max_length=255)
    dish = models.ForeignKey(Dishes)
    order = models.ForeignKey(Order)


class Seat(models.Model):
    num = models.IntegerField(verbose_name=u'人数')


class SeatOrder(models.Model):
    date = models.DateTimeField(verbose_name=u'预约时间')
    contact = models.CharField(verbose_name=u'联系人',max_length=32)
    mobile = models.DecimalField(verbose_name=u'手机号',max_digits=11,decimal_places=0)


class SeatOrderItem(models.Model):
    seat = models.ForeignKey(Seat)
    num = models.IntegerField(verbose_name=u'数量')


class Verification(models.Model):
    time = models.DateTimeField(verbose_name=u'过期时间')
    mobile = models.DecimalField(verbose_name=u'手机号',max_digits=11,decimal_places=0)
    code = models.CharField(verbose_name=u'验证码',max_length=6)
    verified = models.BooleanField(default=False)