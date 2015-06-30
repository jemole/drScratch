# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_csvs_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='csvs',
            options={'get_latest_by': 'date'},
        ),
    ]
