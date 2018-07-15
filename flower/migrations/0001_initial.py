# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllHouse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=255, null=True)),
                ('village', models.CharField(max_length=255, null=True)),
                ('are', models.CharField(max_length=255, null=True)),
                ('type', models.CharField(max_length=255, null=True)),
                ('size', models.CharField(max_length=255, null=True)),
                ('ori', models.CharField(max_length=255, null=True)),
                ('info', models.CharField(max_length=255, null=True)),
                ('rent', models.CharField(max_length=255, null=True)),
                ('people', models.CharField(max_length=255, null=True)),
                ('dist', models.CharField(max_length=255, null=True)),
            ],
        ),
    ]
