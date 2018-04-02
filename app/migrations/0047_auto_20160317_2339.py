# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0046_remove_coder_birthmonth'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coder',
            name='birthyear',
        ),
        migrations.RemoveField(
            model_name='coder',
            name='country',
        ),
        migrations.RemoveField(
            model_name='coder',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='coder',
            name='gender_other',
        ),
    ]
