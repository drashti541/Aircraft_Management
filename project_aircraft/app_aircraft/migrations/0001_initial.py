# Generated by Django 5.0 on 2023-12-14 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('serial_number', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('manufacturer', models.CharField(max_length=100)),
            ],
        ),
    ]