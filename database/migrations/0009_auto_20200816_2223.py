# Generated by Django 3.0.9 on 2020-08-16 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0008_auto_20200816_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chef',
            name='followers',
            field=models.ManyToManyField(related_name='_chef_followers_+', through='database.Follow', to='database.Chef'),
        ),
    ]