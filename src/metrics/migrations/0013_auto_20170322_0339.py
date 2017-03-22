# -*- coding: utf-8 -*-
# Generated by Django 1.11a1 on 2017-03-22 03:39
from __future__ import unicode_literals

from django.db import migrations, models
import metrics.models


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0012_auto_20170224_0633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='doi',
            field=models.CharField(help_text=b'article identifier', max_length=255, unique=True, validators=[metrics.models.validate_doi]),
        ),
    ]
