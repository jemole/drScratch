# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0049_remove_coder_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='coder',
            name='img',
            field=models.ImageField(default=b'app/images/drScratch.png', upload_to=b'img/'),
        ),
    ]
