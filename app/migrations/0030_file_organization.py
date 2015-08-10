# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_auto_20150729_1028'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='organization',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
