# Generated by Django 3.0.3 on 2020-08-11 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0009_category_creater'),
        ('group', '0013_remove_articlegroup_category_groupid'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='articlegroup_category',
            unique_together={('articleID', 'categoryID')},
        ),
        migrations.AlterUniqueTogether(
            name='group_category',
            unique_together={('name', 'group')},
        ),
    ]
