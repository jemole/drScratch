# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0037_file_coder'),
    ]

    operations = [
        migrations.AddField(
            model_name='csvs',
            name='coder',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='csvs',
            name='organization',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='file',
            name='coder',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='file',
            name='organization',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
