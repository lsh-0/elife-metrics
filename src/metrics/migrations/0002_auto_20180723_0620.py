# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-07-23 06:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagetype',
            name='name',
            field=models.CharField(choices=[('blog-article', 'blog-article'), ('event', 'event'), ('interview', 'interview'), ('labs-post', 'labs-post'), ('press-package', 'press-package'), ('collection', 'collection')], max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterUniqueTogether(
            name='pagecount',
            unique_together=set([('page', 'date')]),
        ),
    ]
