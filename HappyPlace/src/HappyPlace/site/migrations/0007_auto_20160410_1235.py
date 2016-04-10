# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site', '0006_auto_20160410_1230'),
    ]

    operations = [
        migrations.RenameField(
            model_name='happyplace',
            old_name='lat',
            new_name='lattitude',
        ),
        migrations.RenameField(
            model_name='happyplace',
            old_name='long',
            new_name='longitude',
        ),
    ]
