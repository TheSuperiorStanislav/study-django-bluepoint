# Generated by Django 2.1.7 on 2019-03-09 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogpost_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='shared_to',
            field=models.ManyToManyField(related_name='shared_posts', to='blog.Blog'),
        ),
    ]
