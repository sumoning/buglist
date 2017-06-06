# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='context',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('auther', models.CharField(max_length=20)),
                ('time', models.DateField()),
                ('details', models.TextField()),
                ('status', models.BooleanField(default=0)),
            ],
        ),
    ]
