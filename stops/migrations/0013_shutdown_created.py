# Generated by Django 3.1.6 on 2021-02-24 18:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('stops', '0012_auto_20210224_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='shutdown',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
