# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0035_auto_20151006_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coder',
            name='img',
            field=models.ImageField(default=b'app/images/cat.png', upload_to=b'img/'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='img',
            field=models.ImageField(default=b'app/images/cat.png', upload_to=b'img/'),
        ),
    ]
