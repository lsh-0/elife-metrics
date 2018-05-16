# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-05 01:02
from __future__ import unicode_literals

from django.db import migrations, models
import article_metrics.models


class Migration(migrations.Migration):

    dependencies = [
        ('article_metrics', '0015_auto_20170517_0554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='doi',
            field=models.CharField(help_text='article identifier', max_length=255, unique=True, validators=[article_metrics.models.validate_doi]),
        ),
        migrations.AlterField(
            model_name='citation',
            name='source',
            field=models.CharField(choices=[('crossref', 'Crossref'), ('pubmed', 'PubMed Central'), ('scopus', 'Scopus')], max_length=10),
        ),
        migrations.AlterField(
            model_name='metric',
            name='abstract',
            field=models.PositiveIntegerField(help_text='article abstract page views'),
        ),
        migrations.AlterField(
            model_name='metric',
            name='date',
            field=models.CharField(blank=True, help_text="the date this metric is for in YYYY-MM-DD, YYYY-MM and YYYY formats or None for 'all time'", max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='metric',
            name='digest',
            field=models.PositiveIntegerField(help_text='article digest page views'),
        ),
        migrations.AlterField(
            model_name='metric',
            name='full',
            field=models.PositiveIntegerField(help_text='article page views'),
        ),
        migrations.AlterField(
            model_name='metric',
            name='pdf',
            field=models.PositiveIntegerField(help_text='pdf downloads'),
        ),
        migrations.AlterField(
            model_name='metric',
            name='period',
            field=models.CharField(choices=[('day', 'Daily'), ('month', 'Monthly'), ('ever', 'All time')], max_length=10),
        ),
        migrations.AlterField(
            model_name='metric',
            name='source',
            field=models.CharField(choices=[('ga', 'Google Analytics'), ('hw', 'Highwire')], max_length=2),
        ),
    ]
