# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0042_discuss'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discuss',
            name='comment',
            field=models.TextField(max_length=150),
        ),
    ]
