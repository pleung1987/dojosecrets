# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 19:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_auto_20170222_0719'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=45),
        ),
    ]