# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=50)),
                ('desc', models.CharField(default=b'', max_length=100, blank=True)),
                ('level', models.CharField(default=b'B', max_length=1, choices=[(b'M', b'Mandatory'), (b'B', b'Basic'), (b'O', b'Optional'), (b'A', b'Advanced')])),
                ('stype', models.CharField(default=b'AN', max_length=2, choices=[(b'A', b'Aphabetic'), (b'N', b'Numeric'), (b'AN', b'Alpha Numeric'), (b'P', b'Password'), (b'IP', b'IPv4 Address'), (b'MI', b'Multiple IP Addresses'), (b'C', b'Compound Setting'), (b'E', b'Email'), (b'CU', b'Custom')])),
                ('standard_label', models.CharField(default=b'', max_length=50, blank=True)),
                ('value', models.CharField(default=b'', max_length=200, blank=True)),
                ('device', models.ForeignKey(related_name='settings', to='logger.Device')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
