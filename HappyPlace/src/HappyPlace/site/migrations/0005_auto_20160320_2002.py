# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site', '0004_auto_20160318_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='happyplace',
            name='days',
            field=models.CharField(choices=[('S', 'Sunday'), ('M', 'Monday'), ('T', 'Tuesday'), ('W', 'Wednesday'), ('R', 'Thursday'), ('F', 'Friday'), ('Y', 'Saturday')], max_length=100),
            preserve_default=True,
        ),
    ]
