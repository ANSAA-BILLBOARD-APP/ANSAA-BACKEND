# Generated by Django 5.0.4 on 2024-05-14 17:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_asset', '0007_rename_image_billboards_image_1_billboards_image_2_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserZone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('zone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='media_asset.zones')),
            ],
            options={
                'verbose_name': 'User Zone',
                'verbose_name_plural': 'User Zones',
                'unique_together': {('user', 'zone')},
            },
        ),
    ]
