# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_auto_20150930_1543'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='Coder',
        ),
        migrations.RenameModel(
            old_name='UserHash',
            new_name='CoderHash',
        ),
        migrations.AddField(
            model_name='organization',
            name='img',
            field=models.ImageField(default=b'None', upload_to=b'img/'),
        ),
        migrations.AlterField(
            model_name='student',
            name='student',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='teacher',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
