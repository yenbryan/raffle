# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(null=True, upload_to=b'media/product_pictures', blank=True)),
                ('description', models.CharField(max_length=140, null=True, blank=True)),
                ('default_picture', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=140)),
                ('description', models.TextField(null=True, blank=True)),
                ('total_number_of_tickets', models.IntegerField()),
                ('tickets_sold', models.IntegerField()),
                ('end_time', models.DateTimeField()),
                ('start_time', models.DateTimeField()),
                ('pricing_per_ticket', models.DecimalField(max_digits=8, decimal_places=2)),
                ('winning_ticket_number', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ticket_number', models.IntegerField()),
                ('product', models.ForeignKey(related_name='tickets', to='ticketing.Product')),
                ('user', models.ForeignKey(related_name='tickets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='picture',
            name='product',
            field=models.ForeignKey(related_name='pictures', to='ticketing.Product'),
            preserve_default=True,
        ),
    ]
