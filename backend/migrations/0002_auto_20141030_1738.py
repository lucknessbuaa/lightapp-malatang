# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seatorder',
            name='date',
        ),
        migrations.RemoveField(
            model_name='seatorderitem',
            name='end',
        ),
        migrations.RemoveField(
            model_name='seatorderitem',
            name='start',
        ),
        migrations.AddField(
            model_name='seatorder',
            name='end',
            field=models.DateTimeField(null=True, verbose_name='\u7ed3\u675f\u65f6\u95f4', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='seatorder',
            name='start',
            field=models.DateTimeField(null=True, verbose_name='\u8d77\u59cb\u65f6\u95f4', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='seatorder',
            name='status',
            field=models.IntegerField(default=0, verbose_name='\u72b6\u6001'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='seatorder',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 30, 17, 38, 14, 834072), verbose_name='\u4e0b\u5355\u65f6\u95f4', auto_now_add=True),
            preserve_default=False,
        ),
    ]
