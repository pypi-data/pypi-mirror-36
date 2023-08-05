# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-20 03:49
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flow', '0012_recreate_empty_parents'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataMigrationHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('migration', models.CharField(db_index=True, max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('metadata', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='migration_history', to='flow.Data')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProcessMigrationHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('migration', models.CharField(db_index=True, max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('metadata', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='migration_history', to='flow.Process')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
