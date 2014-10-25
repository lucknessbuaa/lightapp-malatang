# coding: utf-8

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Dishes(models.Model):
    desc = models.TextField(verbose_name=u'介绍')
    cover = models.URLField(verbose_name=u'截图')
    name = models.CharField(verbose_name=u'名称', max_length=255)
    price = models.DecimalField(verbose_name=u'价格', max_digits=11, decimal_places=2)
    removed = models.BooleanField(default=False)


class Order(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(verbose_name=u'订餐时间',auto_now_add=True, blank=True)
    deadline = models.DateTimeField(verbose_name=u'送餐时间',blank=True)
    complete = models.DateTimeField(verbose_name=u'送达时间',blank=True,null=True)
    location = models.TextField(verbose_name=u'地点')
    contact = models.CharField(verbose_name=u'联系人',max_length=32)
    mobile = models.CharField(verbose_name=u'手机号',max_length=11)
    number = models.SmallIntegerField(verbose_name=u'人数') # 餐具？
    total = models.DecimalField(verbose_name=u'总价', max_digits=11, decimal_places=2)
    count = models.IntegerField(verbose_name=u'份数')


class OrderItem(models.Model):
    price = models.DecimalField(verbose_name=u'合计', max_digits=11, decimal_places=2)
    count = models.IntegerField(verbose_name=u'份数')
    name = models.CharField(verbose_name=u'名称', max_length=255)
    dish = models.ForeignKey(Dishes)
    order = models.ForeignKey(Order)


class SeatOrder(models.Model):
    user = models.ForeignKey(User)
    time = models.DateTimeField(verbose_name=u'下单时间',auto_now_add=True)
    start = models.DateTimeField(verbose_name=u'起始时间',blank=True,null=True)
    end = models.DateTimeField(verbose_name=u'结束时间',blank=True,null=True)
    contact = models.CharField(verbose_name=u'联系人',max_length=32)
    mobile = models.CharField(verbose_name=u'手机号',max_length=11)
    number = models.IntegerField(verbose_name=u'数量')
    ticket = models.CharField(verbose_name=u'预约号',max_length=8)

    @property
    def finished(self):
        from datetime import datetime
        if not self.end : 
            return False
        return self.end < datetime.now()


class Seat(models.Model):
    reserved = models.BooleanField(default=False) # reserved for other usages
    ordered = models.IntegerField(verbose_name=u'次数')


class SeatOrderItem(models.Model):
    seat = models.ForeignKey(Seat)
    seatOrder = models.ForeignKey(SeatOrder)
    ended = models.BooleanField(default=False)


class Verification(models.Model):
    time = models.DateTimeField(verbose_name=u'过期时间')
    mobile = models.CharField(verbose_name=u'手机号',max_length=11)
    code = models.CharField(verbose_name=u'验证码',max_length=6)
    usable = models.BooleanField(default=True)
