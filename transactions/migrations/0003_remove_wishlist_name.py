# Generated by Django 3.1.7 on 2021-02-22 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_auto_20210222_1852'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='name',
        ),
    ]
