# Generated by Django 3.0.7 on 2020-06-12 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_auto_20200612_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ImageField(null=True, upload_to='', verbose_name='Resim'),
        ),
    ]
