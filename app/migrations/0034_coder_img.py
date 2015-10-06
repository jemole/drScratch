# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0033_auto_20151002_0828'),
    ]

    operations = [
        migrations.AddField(
            model_name='coder',
            name='img',
            field=models.ImageField(default=b'None', upload_to=b'img/'),
        ),
    ]
