# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-07-02 15:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0006_auto_20180702_0211'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='player',
            unique_together=set([('match', 'heroid')]),
        ),
    ]