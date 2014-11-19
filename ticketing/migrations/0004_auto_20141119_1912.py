# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0003_auto_20141119_0114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='picture',
            name='default_picture',
        ),
        migrations.AddField(
            model_name='product',
            name='default_picture',
            field=models.ForeignKey(related_name='products', blank=True, to='ticketing.Picture', null=True),
            preserve_default=True,
        ),
    ]
