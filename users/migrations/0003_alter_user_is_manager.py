# Generated by Django 4.2.2 on 2023-07-27 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_notification_channel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_manager',
            field=models.BooleanField(db_index=True, default=False, verbose_name='MediaUploadX Manager'),
        ),
    ]
