# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site', '0008_auto_20160413_2134'),
    ]

    operations = [
        migrations.RenameField(
            model_name='happyhour',
            old_name='happyPlaceId',
            new_name='happyPlace',
        ),
    ]
