# Generated by Django 3.2.9 on 2022-02-16 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_post', '0002_remove_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='static/category_icons'),
        ),
    ]
