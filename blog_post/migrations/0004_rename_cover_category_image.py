# Generated by Django 3.2.9 on 2022-02-18 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_post', '0003_category_cover'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='cover',
            new_name='image',
        ),
    ]
