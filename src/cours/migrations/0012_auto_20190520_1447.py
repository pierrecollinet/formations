# Generated by Django 2.2 on 2019-05-20 14:47

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('cours', '0011_formateurcours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cours',
            name='courte_description',
            field=tinymce.models.HTMLField(),
        ),
        migrations.AlterField(
            model_name='cours',
            name='long_description',
            field=tinymce.models.HTMLField(),
        ),
    ]