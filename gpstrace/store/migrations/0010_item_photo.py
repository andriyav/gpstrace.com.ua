# Generated by Django 4.0.4 on 2022-06-04 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_category_slug_alter_category_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='photo',
            field=models.ImageField(null=True, upload_to='img'),
        ),
    ]
