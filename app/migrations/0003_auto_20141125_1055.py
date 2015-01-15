# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='docfile',
            field=models.FileField(default=datetime.datetime(2014, 11, 25, 10, 55, 1, 98657, tzinfo=utc), upload_to=b'documents/%Y/%m/%d'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='file',
            name='filename',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
    ]
