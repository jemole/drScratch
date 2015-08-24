# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_auto_20150527_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='language',
            field=models.TextField(default=b'en'),
            preserve_default=True,
        ),
    ]
