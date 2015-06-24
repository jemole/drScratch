# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_auto_20150623_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='email',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='hashkey',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='password',
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
