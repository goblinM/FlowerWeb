# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flower', '0005_auto_20180715_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realtimepens',
            name='code',
            field=models.CharField(max_length=255, unique=True, null=True),
        ),
    ]
