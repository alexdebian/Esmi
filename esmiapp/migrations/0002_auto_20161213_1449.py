# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-13 11:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('esmiapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='esminews',
            name='typeartical',
            field=models.CharField(choices=[('f', 'free'), ('c', 'close')], help_text='Тип материала', max_length=1),
        ),
    ]
