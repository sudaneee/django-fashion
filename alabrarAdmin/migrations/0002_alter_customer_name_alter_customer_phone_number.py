# Generated by Django 4.1.1 on 2022-09-13 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alabrarAdmin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(max_length=200),
        ),
    ]
