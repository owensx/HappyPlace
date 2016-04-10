# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site', '0005_auto_20160320_2002'),
    ]

    operations = [
        migrations.AddField(
            model_name='happyplace',
            name='lat',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='happyplace',
            name='long',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
    ]
