# Generated by Django 2.2 on 2019-06-06 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cours', '0024_option_salle'),
    ]

    operations = [
        migrations.AddField(
            model_name='cours',
            name='moyenne_review',
            field=models.CharField(default='5', max_length=20),
        ),
    ]
