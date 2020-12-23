# Generated by Django 3.0.7 on 2020-06-18 16:13

import article.models
import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0020_auto_20200614_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, default='default/61733.png', null=True, upload_to=article.models.upload_to, verbose_name='Resim'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_author_email',
            field=models.EmailField(max_length=254, null=True, verbose_name='E-Mail'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_content',
            field=ckeditor.fields.RichTextField(max_length=2000, null=True, verbose_name='Yorum'),
        ),
    ]