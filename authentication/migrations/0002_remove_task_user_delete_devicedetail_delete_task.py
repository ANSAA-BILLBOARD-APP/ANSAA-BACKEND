# Generated by Django 5.0.4 on 2024-06-03 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='user',
        ),
        migrations.DeleteModel(
            name='DeviceDetail',
        ),
        migrations.DeleteModel(
            name='Task',
        ),
    ]