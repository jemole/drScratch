# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0024_organizationhash'),
    ]

    operations = [
        migrations.CreateModel(
            name='CSVs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=100)),
                ('directory', models.CharField(max_length=100)),
                ('organization', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='organization',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.RemoveField(
            model_name='organization',
            name='email',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='id',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='name',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='password',
        ),
        migrations.AddField(
            model_name='organization',
            name='user_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=10000, serialize=False, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
