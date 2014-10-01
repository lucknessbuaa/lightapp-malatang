# coding: utf-8

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

ACTIVITY_CHOICES = (
    ('ad', u'广告'),
    ('activity', u'活动'),
    ('announcement', u'公告')
)

class News(models.Model):
    type = models.CharField(verbose_name=u'类型', choices=ACTIVITY_CHOICES, max_length=20)
    content = models.TextField(verbose_name=u'内容')
    title = models.CharField(verbose_name=u'标题', max_length=255)


class Participants(models.Model):
    user = models.ForeignKey(User)
    news = models.ForeignKey(News)


class Feedback(models.Model):
    message = models.CharField(verbose_name=u'信息', max_length=255)
    user = models.ForeignKey(User)


