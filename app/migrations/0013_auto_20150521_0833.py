# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20150521_0827'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='email',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teacher',
            name='password',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teacher',
            name='username',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
