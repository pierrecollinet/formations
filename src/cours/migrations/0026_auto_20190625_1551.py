# Generated by Django 2.2 on 2019-06-25 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cours', '0025_cours_moyenne_review'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reviewcours',
            options={'ordering': ('-rating',)},
        ),
    ]
