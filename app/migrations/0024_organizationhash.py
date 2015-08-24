# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_auto_20150621_2144'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationHash',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hashkey', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
