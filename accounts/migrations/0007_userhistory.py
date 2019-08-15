# Generated by Django 2.2.4 on 2019-08-14 14:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20190814_1847'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_name', models.CharField(max_length=30)),
                ('rate_of_return', models.CharField(max_length=10)),
                ('total_assets', models.CharField(max_length=100)),
                ('amount_of_asset_change', models.CharField(max_length=100)),
                ('trade_numbers', models.CharField(max_length=100)),
                ('john_bur_term', models.CharField(max_length=10)),
                ('game_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
