# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_coder_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coder',
            name='img',
            field=models.ImageField(default=b'app/imges/cat.png', upload_to=b'img/'),
        ),
    ]
