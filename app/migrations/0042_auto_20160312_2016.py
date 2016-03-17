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
                ('date', models.DateTimeField()),
                ('comment', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='attribute',
            name='myproject',
        ),
        migrations.DeleteModel(
            name='Classroom',
        ),
        migrations.DeleteModel(
            name='CoderHash',
        ),
        migrations.RemoveField(
            model_name='dead',
            name='myproject',
        ),
        migrations.RemoveField(
            model_name='duplicate',
            name='myproject',
        ),
        migrations.RemoveField(
            model_name='mastery',
            name='myproject',
        ),
        migrations.RemoveField(
            model_name='project',
            name='dashboard',
        ),
        migrations.RemoveField(
            model_name='sprite',
            name='myproject',
        ),
        migrations.DeleteModel(
            name='Attribute',
        ),
        migrations.DeleteModel(
            name='Dashboard',
        ),
        migrations.DeleteModel(
            name='Dead',
        ),
        migrations.DeleteModel(
            name='Duplicate',
        ),
        migrations.DeleteModel(
            name='Mastery',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
        migrations.DeleteModel(
            name='Sprite',
        ),
    ]
