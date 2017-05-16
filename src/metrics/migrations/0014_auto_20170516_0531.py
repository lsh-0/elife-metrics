# -*- coding: utf-8 -*-
# Generated by Django 1.11a1 on 2017-05-16 05:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0013_auto_20170322_0339'),
    ]

    operations = [
        migrations.AddField(
            model_name='citation',
            name='datetime_record_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='citation',
            name='datetime_record_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='metric',
            name='datetime_record_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='metric',
            name='datetime_record_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
