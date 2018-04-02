# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0042_auto_20160312_2016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coder',
            name='hashkey',
        ),
        migrations.AddField(
            model_name='coder',
            name='birthmonth',
            field=models.CharField(default=datetime.datetime(2016, 3, 12, 22, 20, 30, 800931, tzinfo=utc), max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coder',
            name='birthyear',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coder',
            name='country',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coder',
            name='gender',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coder',
            name='gender_other',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
