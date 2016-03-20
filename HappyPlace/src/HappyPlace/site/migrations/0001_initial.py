# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HappyPlace',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=75)),
                ('notes', models.CharField(max_length=200)),
                ('site', models.CharField(max_length=50)),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
