# Generated by Django 2.2 on 2019-06-06 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partenaires', '0001_initial'),
        ('cours', '0023_auto_20190606_0912'),
    ]

    operations = [
        migrations.AddField(
            model_name='option',
            name='salle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='partenaires.SalleCours'),
        ),
    ]
