# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0048_auto_20160317_2340'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coder',
            name='img',
        ),
    ]
