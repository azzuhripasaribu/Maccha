# Generated by Django 4.1 on 2022-10-25 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menumodel',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
