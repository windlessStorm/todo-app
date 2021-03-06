# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-19 13:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0002_auto_20181017_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='delete_time',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateField(default=b'2018-10-19'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=2),
        ),
    ]
