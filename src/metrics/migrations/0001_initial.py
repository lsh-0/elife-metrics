# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-14 03:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PageCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('views', models.PositiveIntegerField()),
                ('date', models.DateField()),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='metrics.Page')),
            ],
        ),
        migrations.CreateModel(
            name='PageType',
            fields=[
                ('name', models.CharField(choices=[('blog-article', 'blog-article'), ('event', 'event'), ('interview', 'interview'), ('labs-post', 'labs-post'), ('press-package', 'press-package')], max_length=255, primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='metrics.PageType'),
        ),
        migrations.AlterUniqueTogether(
            name='page',
            unique_together=set([('type', 'identifier')]),
        ),
    ]
