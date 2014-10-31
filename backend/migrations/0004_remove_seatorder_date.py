# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_seatorder_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seatorder',
            name='date',
        ),
    ]
