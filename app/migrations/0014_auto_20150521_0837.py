# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20150521_0833'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='student',
        ),
        migrations.AddField(
            model_name='classroom',
            name='student',
            field=models.ManyToManyField(to='app.Student'),
            preserve_default=True,
        ),
    ]
