# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flower', '0004_realtimepens_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='realtimepens',
            old_name='data',
            new_name='date',
        ),
    ]
