# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='tickets_sold',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
