# Generated by Django 5.1.6 on 2025-02-15 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='latitude',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='longitude',
            field=models.FloatField(null=True),
        ),
    ]
