# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site', '0007_auto_20160410_1235'),
    ]

    operations = [
        migrations.CreateModel(
            name='HappyHour',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('notes', models.CharField(max_length=200)),
                ('days', models.CharField(max_length=100, choices=[('S', 'Sunday'), ('M', 'Monday'), ('T', 'Tuesday'), ('W', 'Wednesday'), ('R', 'Thursday'), ('F', 'Friday'), ('Y', 'Saturday')])),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
                ('happyPlaceId', models.ForeignKey(to='site.HappyPlace')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='happyplace',
            name='days',
        ),
        migrations.RemoveField(
            model_name='happyplace',
            name='end',
        ),
        migrations.RemoveField(
            model_name='happyplace',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='happyplace',
            name='start',
        ),
    ]
