# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dishes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('desc', models.TextField(verbose_name='\u4ecb\u7ecd')),
                ('cover', models.URLField(verbose_name='\u622a\u56fe')),
                ('name', models.CharField(max_length=255, verbose_name='\u540d\u79f0')),
                ('price', models.DecimalField(verbose_name='\u4ef7\u683c', max_digits=11, decimal_places=2)),
                ('removed', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='\u8ba2\u9910\u65f6\u95f4')),
                ('deadline', models.DateTimeField(verbose_name='\u9001\u9910\u65f6\u95f4', blank=True)),
                ('complete', models.DateTimeField(null=True, verbose_name='\u9001\u8fbe\u65f6\u95f4', blank=True)),
                ('location', models.TextField(verbose_name='\u5730\u70b9')),
                ('contact', models.CharField(max_length=32, verbose_name='\u8054\u7cfb\u4eba')),
                ('mobile', models.CharField(max_length=11, verbose_name='\u624b\u673a\u53f7')),
                ('number', models.SmallIntegerField(verbose_name='\u4eba\u6570')),
                ('total', models.DecimalField(verbose_name='\u603b\u4ef7', max_digits=11, decimal_places=2)),
                ('count', models.IntegerField(verbose_name='\u4efd\u6570')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(verbose_name='\u5408\u8ba1', max_digits=11, decimal_places=2)),
                ('count', models.IntegerField(verbose_name='\u4efd\u6570')),
                ('name', models.CharField(max_length=255, verbose_name='\u540d\u79f0')),
                ('dish', models.ForeignKey(to='backend.Dishes')),
                ('order', models.ForeignKey(to='backend.Order')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reserved', models.BooleanField(default=False)),
                ('ordered', models.IntegerField(verbose_name='\u6b21\u6570')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SeatOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(verbose_name='\u9884\u7ea6\u65f6\u95f4')),
                ('contact', models.CharField(max_length=32, verbose_name='\u8054\u7cfb\u4eba')),
                ('mobile', models.CharField(max_length=11, verbose_name='\u624b\u673a\u53f7')),
                ('number', models.IntegerField(verbose_name='\u6570\u91cf')),
                ('ticket', models.CharField(max_length=8, verbose_name='\u9884\u7ea6\u53f7')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SeatOrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField(null=True, verbose_name='\u8d77\u59cb\u65f6\u95f4', blank=True)),
                ('end', models.DateTimeField(null=True, verbose_name='\u7ed3\u675f\u65f6\u95f4', blank=True)),
                ('ended', models.BooleanField(default=False)),
                ('seat', models.ForeignKey(to='backend.Seat')),
                ('seatOrder', models.ForeignKey(to='backend.SeatOrder')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(verbose_name='\u8fc7\u671f\u65f6\u95f4')),
                ('mobile', models.CharField(max_length=11, verbose_name='\u624b\u673a\u53f7')),
                ('code', models.CharField(max_length=6, verbose_name='\u9a8c\u8bc1\u7801')),
                ('usable', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
