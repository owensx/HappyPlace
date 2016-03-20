# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site', '0002_happyplace_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='happyplace',
            name='active',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
