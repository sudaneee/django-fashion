# Generated by Django 4.1.1 on 2022-09-24 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_blog_gallery_generalinformation_paragraph_service_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='sliders')),
                ('tag', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]
