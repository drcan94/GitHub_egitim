# Generated by Django 3.0.7 on 2020-06-23 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0027_favoritearticle'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favoritearticle',
            options={'verbose_name_plural': 'Favori Spotlar'},
        ),
        migrations.AlterField(
            model_name='favoritearticle',
            name='article',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favorite_article', to='article.Article', verbose_name='Favori Spot'),
        ),
    ]
