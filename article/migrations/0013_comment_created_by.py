# Generated by Django 3.0.3 on 2020-09-08 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0002_remove_userprofile_userindex'),
        ('article', '0012_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='personal.UserProfile'),
        ),
    ]
