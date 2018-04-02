# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0047_auto_20160317_2339'),
    ]

    operations = [
        migrations.AddField(
            model_name='coder',
            name='birthmonth',
            field=models.CharField(default=0, max_length=100),
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
