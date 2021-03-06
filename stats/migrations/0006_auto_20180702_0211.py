# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-07-02 06:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0005_auto_20180423_1700'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rad', models.BooleanField()),
                ('heroid', models.CharField(default='novalue', max_length=255)),
                ('playerid', models.CharField(default='novalue', max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='match',
        ),
        migrations.RemoveField(
            model_name='match',
            name='dire1_heroid',
        ),
        migrations.RemoveField(
            model_name='match',
            name='dire1_playerid',
        ),
        migrations.RemoveField(
            model_name='match',
            name='dire2_heroid',
        ),
        migrations.RemoveField(
            model_name='match',
            name='dire2_playerid',
        ),
        migrations.RemoveField(
            model_name='match',
            name='dire3_heroid',
        ),
        migrations.RemoveField(
            model_name='match',
            name='dire3_playerid',
        ),
        migrations.RemoveField(
            model_name='match',
            name='dire4_heroid',
        ),
        migrations.RemoveField(
            model_name='match',
            name='dire4_playerid',
        ),
        migrations.RemoveField(
            model_name='match',
            name='dire5_heroid',
        ),
        migrations.RemoveField(
            model_name='match',
            name='dire5_playerid',
        ),
        migrations.RemoveField(
            model_name='match',
            name='rad1_heroid',
        ),
        migrations.RemoveField(
            model_name='match',
            name='rad1_playerid',
        ),
        migrations.RemoveField(
            model_name='match',
            name='rad2_heroid',
        ),
        migrations.RemoveField(
            model_name='match',
            name='rad2_playerid',
        ),
        migrations.RemoveField(
            model_name='match',
            name='rad3_heroid',
        ),
        migrations.RemoveField(
            model_name='match',
            name='rad3_playerid',
        ),
        migrations.RemoveField(
            model_name='match',
            name='rad4_heroid',
        ),
        migrations.RemoveField(
            model_name='match',
            name='rad4_playerid',
        ),
        migrations.RemoveField(
            model_name='match',
            name='rad5_heroid',
        ),
        migrations.RemoveField(
            model_name='match',
            name='rad5_playerid',
        ),
        migrations.DeleteModel(
            name='Inventory',
        ),
        migrations.AddField(
            model_name='player',
            name='match',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='stats.Match'),
        ),
    ]
