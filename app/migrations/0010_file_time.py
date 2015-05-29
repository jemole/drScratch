# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_file_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='time',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
