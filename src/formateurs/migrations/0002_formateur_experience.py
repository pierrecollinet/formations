# Generated by Django 2.2 on 2019-05-16 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formateurs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='formateur',
            name='experience',
            field=models.TextField(blank=True, null=True),
        ),
    ]
