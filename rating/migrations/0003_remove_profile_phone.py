# Generated by Django 3.1.5 on 2021-01-24 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0002_auto_20210124_1258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='phone',
        ),
    ]