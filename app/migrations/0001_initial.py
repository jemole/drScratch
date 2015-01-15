# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('character', models.TextField()),
                ('orientation', models.IntegerField()),
                ('position', models.IntegerField()),
                ('costume', models.IntegerField()),
                ('visibility', models.IntegerField()),
                ('size', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.TextField()),
                ('text', models.TextField()),
                ('date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.TextField()),
                ('frelease', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dead',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('character', models.TextField()),
                ('blocks', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Duplicate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numduplicates', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Mastery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('abstraction', models.IntegerField()),
                ('paralel', models.IntegerField()),
                ('logic', models.IntegerField()),
                ('synchronization', models.IntegerField()),
                ('flowcontrol', models.IntegerField()),
                ('interactivity', models.IntegerField()),
                ('representation', models.IntegerField()),
                ('scoring', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('version', models.IntegerField()),
                ('score', models.IntegerField()),
                ('level', models.TextField()),
                ('path', models.TextField()),
                ('fupdate', models.TextField()),
                ('dashboard', models.ForeignKey(to='app.Dashboard')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sprite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('character', models.TextField()),
                ('myproject', models.ForeignKey(to='app.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='mastery',
            name='myproject',
            field=models.ForeignKey(to='app.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='duplicate',
            name='myproject',
            field=models.ForeignKey(to='app.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dead',
            name='myproject',
            field=models.ForeignKey(to='app.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attribute',
            name='myproject',
            field=models.ForeignKey(to='app.Project'),
            preserve_default=True,
        ),
    ]
