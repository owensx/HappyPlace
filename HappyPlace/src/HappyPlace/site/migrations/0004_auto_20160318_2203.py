# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site', '0003_happyplace_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='happyplace',
            name='city',
            field=models.CharField(default='NYC', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='happyplace',
            name='cross',
            field=models.CharField(null=True, max_length=50),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='happyplace',
            name='neighborhood',
            field=models.CharField(null=True, max_length=50),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='happyplace',
            name='phone',
            field=models.CharField(null=True, max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='happyplace',
            name='days',
            field=models.CharField(choices=[('S', 'Sunday'), ('M', 'Monday'), ('T', 'Tuesday'), ('W', 'Wednesday'), ('R', 'Thursday'), ('F', 'Friday'), ('Y', 'Saturday')], default='S', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='happyplace',
            name='site',
            field=models.CharField(null=True, max_length=50),
            preserve_default=True,
        ),
    ]
