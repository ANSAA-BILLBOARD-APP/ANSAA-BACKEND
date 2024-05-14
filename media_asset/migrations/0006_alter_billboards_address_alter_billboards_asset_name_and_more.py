# Generated by Django 5.0.4 on 2024-05-14 17:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_asset', '0005_alter_zones_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billboards',
            name='address',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='billboards',
            name='asset_name',
            field=models.CharField(editable=False, max_length=10),
        ),
        migrations.AlterField(
            model_name='billboards',
            name='asset_type',
            field=models.CharField(blank=True, choices=[('electronic', 'Electronic'), ('static', 'Static')], max_length=50),
        ),
        migrations.AlterField(
            model_name='billboards',
            name='category',
            field=models.CharField(blank=True, choices=[('free standing signs', 'Free standing signs'), ('projecting signs', 'Projecting signs'), ('wall signs', 'Wall signs'), ('special advertisement', 'Special advertisement')], max_length=50),
        ),
        migrations.AlterField(
            model_name='billboards',
            name='city',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='billboards',
            name='image',
            field=models.ImageField(blank=True, upload_to='billboards/'),
        ),
        migrations.AlterField(
            model_name='billboards',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='billboards',
            name='sub_zone',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='media_asset.zones'),
        ),
        migrations.AlterField(
            model_name='billboards',
            name='vacancy',
            field=models.CharField(blank=True, choices=[('vacant', 'Vacant'), ('occupied', 'Occupied')], default='vacant', max_length=20),
        ),
        migrations.AlterField(
            model_name='billboards',
            name='zone',
            field=models.CharField(blank=True, choices=[('normal zone', 'Normal zone'), ('Restricted zone', 'Restricted zone')], max_length=50),
        ),
    ]
