# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20150527_1042'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='duplicatedScripts',
            new_name='duplicatedScript',
        ),
        migrations.RenameField(
            model_name='file',
            old_name='spritesNaming',
            new_name='spriteNaming',
        ),
    ]
