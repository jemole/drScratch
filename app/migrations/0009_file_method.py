# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_delete_stats'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='method',
            field=models.CharField(default='url', max_length=100),
            preserve_default=False,
        ),
    ]
