# Generated by Django 2.2.5 on 2020-10-10 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0022_article_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
