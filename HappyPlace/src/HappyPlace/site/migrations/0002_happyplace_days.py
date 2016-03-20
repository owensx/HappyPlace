# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='happyplace',
            name='days',
            field=models.CharField(choices=[('S', 'Sunday'), ('M', 'Monday'), ('T', 'Tuesday'), ('W', 'Wednesday'), ('R', 'Thursday'), ('F', 'Friday'), ('Y', 'Saturday')], max_length=10, null=True),
            preserve_default=True,
        ),
    ]
