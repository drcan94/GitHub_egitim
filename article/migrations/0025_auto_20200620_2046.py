# Generated by Django 3.0.7 on 2020-06-20 17:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article', '0024_auto_20200620_1701'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='comment_author_email',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='comment_author_firstname',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='comment_author_lastname',
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_content',
            field=models.TextField(max_length=1000, null=True, verbose_name='Yorum'),
        ),
    ]
