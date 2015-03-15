# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Respond', '0003_auto_20150314_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='ContestURL',
            field=models.CharField(default=b'NOURL', max_length=100),
            preserve_default=True,
        ),
    ]
