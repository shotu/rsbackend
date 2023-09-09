# Generated by Django 4.2.4 on 2023-09-07 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fivep', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fivep',
            name='access_token',
            field=models.CharField(default='your_default_value', max_length=255),
        ),
        migrations.AddField(
            model_name='fivep',
            name='client_code',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='fivep',
            name='jwt_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]