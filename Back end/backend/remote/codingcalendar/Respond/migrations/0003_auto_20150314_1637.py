# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Respond', '0002_auto_20150314_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='Description',
            field=models.CharField(default=b'do attend', max_length=500),
            preserve_default=True,
        ),
    ]
