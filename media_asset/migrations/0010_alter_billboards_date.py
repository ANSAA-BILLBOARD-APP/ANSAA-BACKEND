# Generated by Django 5.0.4 on 2024-05-14 18:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_asset', '0009_billboards_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billboards',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
