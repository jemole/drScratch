# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_file_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='email',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='organization',
            name='hashkey',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='organization',
            name='password',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
