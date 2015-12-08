# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0041_auto_20151025_1025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discuss',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nick', models.TextField()),
                ('email', models.TextField(blank=True)),
                ('date', models.DateField()),
                ('comment', models.TextField()),
            ],
        ),
    ]
