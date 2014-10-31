# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20141030_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='seatorder',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 30, 17, 54, 2, 790052), verbose_name='\u65f6\u95f4', auto_now_add=True),
            preserve_default=False,
        ),
    ]
