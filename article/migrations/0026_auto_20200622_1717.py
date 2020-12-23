# Generated by Django 3.0.7 on 2020-06-22 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0025_auto_20200620_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='kategoriler',
            field=models.ManyToManyField(null=True, related_name='article', to='article.Category'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_content',
            field=models.TextField(max_length=1000, null=True, verbose_name='YORUM'),
        ),
    ]