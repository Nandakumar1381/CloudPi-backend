# Generated by Django 3.2.12 on 2023-06-19 21:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locked', '0002_auto_20230618_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locked',
            name='file',
        ),
        migrations.RemoveField(
            model_name='locked',
            name='name',
        ),
        migrations.RemoveField(
            model_name='locked',
            name='uploaded_at',
        ),
    ]
