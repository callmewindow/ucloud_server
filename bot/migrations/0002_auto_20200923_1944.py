# Generated by Django 3.1.1 on 2020-09-23 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bot',
            name='botCode',
            field=models.TextField(default='无'),
        ),
        migrations.AddField(
            model_name='bot',
            name='botIntro',
            field=models.TextField(default='无'),
        ),
        migrations.AddField(
            model_name='bot',
            name='botStatus',
            field=models.BooleanField(default=False),
        ),
    ]
