# Generated by Django 3.0.9 on 2020-09-06 02:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_auto_20200904_0221'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='original_post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='copy_post', to='database.Post'),
        ),
    ]
