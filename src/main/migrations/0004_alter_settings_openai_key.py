# Generated by Django 4.1.5 on 2023-01-13 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_user_id_settings_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='openai_key',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]