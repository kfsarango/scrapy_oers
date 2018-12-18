# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-12-11 05:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryOers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=175, null=True)),
            ],
            options={
                'db_table': 'category_oers',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Oer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=245, null=True)),
                ('author', models.CharField(blank=True, max_length=445, null=True)),
                ('subjects', models.CharField(blank=True, max_length=445, null=True)),
                ('keywords', models.CharField(blank=True, max_length=445, null=True)),
                ('education_level', models.CharField(blank=True, max_length=145, null=True)),
                ('license', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('url', models.TextField(blank=True, null=True)),
                ('download_link', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'oer',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Pages',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=145, null=True)),
                ('domain', models.CharField(blank=True, max_length=145, null=True)),
                ('link_site', models.CharField(blank=True, max_length=445, null=True)),
            ],
            options={
                'db_table': 'pages',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TypeOer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=75, null=True)),
            ],
            options={
                'db_table': 'type_oer',
                'managed': False,
            },
        ),
    ]