# Generated by Django 3.0.3 on 2020-06-28 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0002_delete_articlegroup'),
        ('article', '0003_auto_20200626_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='group',
            field=models.ManyToManyField(null=True, to='group.group'),
        ),
    ]
