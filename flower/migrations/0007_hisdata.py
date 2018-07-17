# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flower', '0006_auto_20180715_2233'),
    ]

    operations = [
        migrations.CreateModel(
            name='HISData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('code', models.CharField(max_length=255, null=True)),
                ('open', models.CharField(max_length=255, null=True)),
                ('high', models.CharField(max_length=255, null=True)),
                ('close', models.CharField(max_length=255, null=True)),
                ('low', models.CharField(max_length=255, null=True)),
                ('volume', models.CharField(max_length=255, null=True)),
                ('price_change', models.CharField(max_length=255, null=True)),
                ('p_change', models.CharField(max_length=255, null=True)),
                ('ma5', models.CharField(max_length=255, null=True)),
                ('ma10', models.CharField(max_length=255, null=True)),
                ('ma20', models.CharField(max_length=255, null=True)),
                ('v_ma5', models.CharField(max_length=255, null=True)),
                ('v_ma10', models.CharField(max_length=255, null=True)),
                ('v_ma20', models.CharField(max_length=255, null=True)),
            ],
        ),
    ]
