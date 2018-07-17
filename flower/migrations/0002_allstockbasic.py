# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flower', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllStockBasic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('code', models.CharField(max_length=255, null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('industry', models.CharField(max_length=255, null=True)),
                ('area', models.CharField(max_length=255, null=True)),
                ('pe', models.CharField(max_length=255, null=True)),
                ('outstanding', models.CharField(max_length=255, null=True)),
                ('totals', models.CharField(max_length=255, null=True)),
                ('totalAssets', models.CharField(max_length=255, null=True)),
                ('liquidAssets', models.CharField(max_length=255, null=True)),
                ('fixedAssets', models.CharField(max_length=255, null=True)),
                ('reserved', models.CharField(max_length=255, null=True)),
                ('reservedPerShare', models.CharField(max_length=255, null=True)),
                ('esp', models.CharField(max_length=255, null=True)),
                ('bvps', models.CharField(max_length=255, null=True)),
                ('pb', models.CharField(max_length=255, null=True)),
                ('timeToMarket', models.CharField(max_length=255, null=True)),
                ('undp', models.CharField(max_length=255, null=True)),
                ('perundp', models.CharField(max_length=255, null=True)),
                ('rev', models.CharField(max_length=255, null=True)),
                ('profit', models.CharField(max_length=255, null=True)),
                ('gpr', models.CharField(max_length=255, null=True)),
                ('npr', models.CharField(max_length=255, null=True)),
                ('holders', models.CharField(max_length=255, null=True)),
            ],
        ),
    ]
