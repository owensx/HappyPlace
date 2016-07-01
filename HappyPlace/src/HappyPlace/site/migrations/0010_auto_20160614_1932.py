# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site', '0009_auto_20160413_2137'),
    ]

    operations = [
        migrations.RenameField(
            model_name='happyplace',
            old_name='lattitude',
            new_name='latitude',
        ),
        migrations.AlterField(
            model_name='happyplace',
            name='city',
            field=models.ForeignKey(related_name='happyPlaces', to='site.City'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('offset', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='happyhour',
            name='happyPlace',
            field=models.ForeignKey(to='site.HappyPlace', related_name='happyHours'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='happyplace',
            name='neighborhood',
            field=models.CharField(default='fill', max_length=50),
            preserve_default=False,
        ),
    ]
