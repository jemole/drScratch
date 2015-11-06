# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0040_auto_20151021_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coder',
            name='img',
            field=models.ImageField(default=b'app/images/drScratch.png', upload_to=b'img/'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='img',
            field=models.ImageField(default=b'app/images/drScratch.png', upload_to=b'img/'),
        ),
    ]
