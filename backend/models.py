# coding: utf-8

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Dishes(models.Model):
    desc = models.TextField(verbose_name=u'介绍')
    cover = models.URLField(verbose_name=u'截图')
    name = models.CharField(verbose_name=u'名称', max_length=255)
    prize = models.DecimalField(verbose_name=u'价格', max_digits=19, decimal_places=10)
    removed = models.BooleanField()


class Seat(models.Model):
    num = models.IntegerField(verbose_name=u'人数')


class Order(models.Model):
    date = models.DateTimeField(verbose_name=u'订餐时间')
    deadline = models.DateTimeField(verbose_name=u'送餐时间')


class OrderItem(models.Model):
    prize = models.DecimalField(verbose_name=u'价格', max_digits=19, decimal_places=10)
    dish = models.ForeignKey(Dishes)
    order = models.ForeignKey(Order)


class SeatOrder(models.Model):
    date = models.DateTimeField(verbose_name=u'时间')


class SeatOrderItem(models.Model):
    seat = models.ForeignKey(Seat)
    num = models.IntegerField(verbose_name=u'数量')

