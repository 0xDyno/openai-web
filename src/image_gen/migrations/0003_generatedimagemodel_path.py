# Generated by Django 4.1.5 on 2023-01-15 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_gen', '0002_rename_imagemodel_generatedimagemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='generatedimagemodel',
            name='path',
            field=models.CharField(default='images/', max_length=200),
        ),
    ]
