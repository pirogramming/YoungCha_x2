# Generated by Django 2.2.4 on 2019-08-17 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20190817_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='wallet',
            field=models.IntegerField(default=10000000),
        ),
    ]