# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-12 20:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0010_auto_20180312_1605'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('tid', models.CharField(default='novalue', max_length=10)),
                ('tindex', models.CharField(default='novalue', max_length=10)),
                ('tname', models.CharField(default='novalue', max_length=30)),
            ],
        ),
        migrations.AlterField(
            model_name='match',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.Tournament'),
        ),
        migrations.DeleteModel(
            name='Tournamente',
        ),
    ]
