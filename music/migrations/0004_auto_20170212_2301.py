# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-12 23:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_lists'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lists',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='lists',
            name='modified_date',
        ),
    ]
