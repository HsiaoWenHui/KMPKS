# Generated by Django 2.2.5 on 2020-10-02 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0018_group_privacy'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='announcement',
            field=models.TextField(null=True),
        ),
    ]