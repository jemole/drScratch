# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0043_auto_20151214_1124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discuss',
            name='email',
        ),
        migrations.AlterField(
            model_name='discuss',
            name='comment',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='discuss',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
