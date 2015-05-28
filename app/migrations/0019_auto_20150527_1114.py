# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20150527_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='abstraction',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='file',
            name='dataRepresentation',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='file',
            name='deadCode',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='file',
            name='duplicatedScript',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='file',
            name='flowControl',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='file',
            name='initialization',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='file',
            name='logic',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='file',
            name='parallelization',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='file',
            name='spriteNaming',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='file',
            name='synchronization',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='file',
            name='userInteractivity',
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
