# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20150527_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='duplicatedScript',
            field=models.CharField(max_length=10),
            preserve_default=True,
        ),
    ]
