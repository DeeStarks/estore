# Generated by Django 3.1.7 on 2021-03-03 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_auto_20210303_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='review_text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
