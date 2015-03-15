# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Respond', '0004_auto_20150314_1824'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='id',
        ),
        migrations.AddField(
            model_name='dataset',
            name='ID',
            field=models.AutoField(default=333, serialize=False, primary_key=True),
            preserve_default=False,
        ),
    ]
