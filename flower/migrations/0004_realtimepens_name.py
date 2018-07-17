# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flower', '0003_realtimepens'),
    ]

    operations = [
        migrations.AddField(
            model_name='realtimepens',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
