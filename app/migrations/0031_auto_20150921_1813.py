# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_file_organization'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('daily_score', models.TextField()),
                ('basic', models.TextField(default=b'')),
                ('development', models.TextField(default=b'')),
                ('master', models.TextField(default=b'')),
                ('daily_projects', models.TextField(default=b'')),
                ('parallelism', models.IntegerField(default=0)),
                ('abstraction', models.IntegerField(default=0)),
                ('logic', models.IntegerField(default=0)),
                ('synchronization', models.IntegerField(default=0)),
                ('flowControl', models.IntegerField(default=0)),
                ('userInteractivity', models.IntegerField(default=0)),
                ('dataRepresentation', models.IntegerField(default=0)),
                ('deadCode', models.IntegerField(default=0)),
                ('duplicateScript', models.IntegerField(default=0)),
                ('spriteNaming', models.IntegerField(default=0)),
                ('initialization', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterModelManagers(
            name='organization',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
