# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-12 20:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0012_auto_20180312_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='tid',
            field=models.CharField(default='novalue', max_length=10),
        ),
    ]
