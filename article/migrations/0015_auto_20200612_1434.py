# Generated by Django 3.0.7 on 2020-06-12 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0014_article_yayin_taslak'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='yayin_taslak',
            field=models.CharField(choices=[(None, 'Yayın Türü Seçiniz'), ('yayin', 'YAYIN'), ('taslak', 'TASLAK')], max_length=6, null=True),
        ),
    ]
