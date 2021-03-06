# Generated by Django 3.0.3 on 2020-08-10 03:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0004_member_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='articleGroup_category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='未分類', max_length=100)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='group.group')),
            ],
        ),
        migrations.AddField(
            model_name='articlegroup',
            name='categoriess',
            field=models.ManyToManyField(to='group.articleGroup_category'),
        ),
    ]
