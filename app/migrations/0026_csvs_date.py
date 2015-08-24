# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_auto_20150630_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='csvs',
            name='date',
            field=models.DateField(default=datetime.datetime.now),
            preserve_default=True,
        ),
    ]
