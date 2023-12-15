# Generated by Django 5.0 on 2023-12-14 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_aircraft', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='aircraft',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='aircraft',
            name='serial_number',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
