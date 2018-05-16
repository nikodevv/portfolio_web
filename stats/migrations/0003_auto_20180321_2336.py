# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-22 03:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0002_auto_20180312_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='dire_teamid',
            field=models.CharField(default='novalue', max_length=30),
        ),
        migrations.AlterField(
            model_name='match',
            name='rad_teamid',
            field=models.CharField(default='novalue', max_length=30),
        ),
        migrations.AlterField(
            model_name='match',
            name='tournament',
            field=models.ForeignKey(blank=True, default=0, on_delete=django.db.models.deletion.CASCADE, to='stats.Tournament'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tournament',
            name='tid',
            field=models.CharField(default='novalue', max_length=30),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='tindex',
            field=models.CharField(default='novalue', max_length=30),
        ),
    ]