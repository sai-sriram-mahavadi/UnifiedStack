# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConsoleLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('console_message', models.CharField(default=b'', max_length=100, blank=True)),
                ('console_summary', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('desc', models.CharField(max_length=200, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.CharField(default=b'I', max_length=1, choices=[(b'I', b'Info'), (b'C', b'Commit'), (b'W', b'Warning'), (b'E', b'Error')])),
                ('timestamp', models.DateTimeField(auto_now=True, verbose_name=b'Log Time')),
                ('message', models.CharField(max_length=200)),
                ('device', models.ForeignKey(related_name=b'logs', to='logger.Device')),
            ],
            options={
                'ordering': ('timestamp',),
            },
            bases=(models.Model,),
        ),
    ]
