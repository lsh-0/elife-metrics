# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0002_auto_20150918_1516'),
    ]

    operations = [
        migrations.RenameField(
            model_name='GAMetric',
            old_name='type',
            new_name='period'
        ),
    ]
