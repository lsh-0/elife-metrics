# -*- coding: utf-8 -*-
# Generated by Django 1.11a1 on 2017-02-01 18:35


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article_metrics', '0010_auto_20170131_1854'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ('-doi',)},
        ),
    ]
