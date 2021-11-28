# Generated by Django 3.1.2 on 2020-10-31 19:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_post', '0007_auto_20201030_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('Film', 'film'), ('Sanat', 'sanat'), ('Müzik', 'müzik')], max_length=5),
        ),
        migrations.AlterField(
            model_name='post',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 31, 22, 20, 3, 803453)),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.TextField(default='Slug is a newspaper term.\n                                                    A slug is a short label for something, containing only letters,\n                                                    numbers, underscores or hyphens. They’re generally used in URLs.', max_length=350),
        ),
    ]
