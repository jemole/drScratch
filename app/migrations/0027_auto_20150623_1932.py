# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_auto_20150623_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationhash',
            name='hashkey',
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
