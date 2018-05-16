# -*- coding: utf-8 -*-
# Generated by Django 1.11a1 on 2017-01-30 17:56


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_metrics', '0008_auto_20170125_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='pmcid',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='pmid',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
