# Generated by Django 2.2.5 on 2020-10-04 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0021_auto_20200930_1915'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='img',
            field=models.CharField(default='/static/img/default0.jpg/', max_length=255),
        ),
    ]
