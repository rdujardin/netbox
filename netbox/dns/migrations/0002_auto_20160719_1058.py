# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-19 10:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dns', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='priority',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
