# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_auto_20141030_1811'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='dateq',
            new_name='date',
        ),
    ]
