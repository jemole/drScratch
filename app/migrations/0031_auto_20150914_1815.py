# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_file_organization'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='organization',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
