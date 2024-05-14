# Generated by Django 5.0.4 on 2024-05-14 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_asset', '0006_alter_billboards_address_alter_billboards_asset_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='billboards',
            old_name='image',
            new_name='image_1',
        ),
        migrations.AddField(
            model_name='billboards',
            name='image_2',
            field=models.ImageField(blank=True, upload_to='billboards/'),
        ),
        migrations.AddField(
            model_name='billboards',
            name='image_3',
            field=models.ImageField(blank=True, upload_to='billboards/'),
        ),
        migrations.AddField(
            model_name='billboards',
            name='main_image',
            field=models.ImageField(blank=True, upload_to='billboards/'),
        ),
    ]
