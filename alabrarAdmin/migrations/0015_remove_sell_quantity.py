# Generated by Django 4.1.1 on 2022-10-10 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alabrarAdmin', '0014_sellsitem_alter_customer_options_sellitemrestock_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sell',
            name='quantity',
        ),
    ]