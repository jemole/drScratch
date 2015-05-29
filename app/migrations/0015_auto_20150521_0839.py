# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20150521_0837'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroom',
            name='student',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='classroom',
        ),
    ]
