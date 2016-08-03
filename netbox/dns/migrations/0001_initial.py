# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-19 10:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ipam', '0004_ipam_vlangroup_uniqueness'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('record_type', models.CharField(max_length=10)),
                ('priority', models.PositiveIntegerField(blank=True)),
                ('value', models.CharField(blank=True, max_length=100)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='records', to='ipam.IPAddress')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('ttl', models.PositiveIntegerField()),
                ('soa_name', models.CharField(max_length=100)),
                ('soa_contact', models.CharField(max_length=100)),
                ('soa_serial', models.CharField(max_length=100)),
                ('soa_refresh', models.PositiveIntegerField()),
                ('soa_retry', models.PositiveIntegerField()),
                ('soa_expire', models.PositiveIntegerField()),
                ('soa_minimum', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='record',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='dns.Zone'),
        ),
    ]
