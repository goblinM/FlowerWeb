# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flower', '0002_allstockbasic'),
    ]

    operations = [
        migrations.CreateModel(
            name='RealTimePens',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('code', models.CharField(max_length=255, null=True)),
                ('open', models.CharField(max_length=255, null=True)),
                ('pre_close', models.CharField(max_length=255, null=True)),
                ('price', models.CharField(max_length=255, null=True)),
                ('high', models.CharField(max_length=255, null=True)),
                ('low', models.CharField(max_length=255, null=True)),
                ('bid', models.CharField(max_length=255, null=True)),
                ('ask', models.CharField(max_length=255, null=True)),
                ('volume', models.CharField(max_length=255, null=True)),
                ('amount', models.CharField(max_length=255, null=True)),
                ('data', models.CharField(max_length=255, null=True)),
                ('time', models.CharField(max_length=255, null=True)),
            ],
        ),
    ]
