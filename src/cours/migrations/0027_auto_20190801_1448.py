# Generated by Django 2.2 on 2019-08-01 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apprenants', '0005_auto_20190801_1213'),
        ('cours', '0026_auto_20190625_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='cours',
            name='faculte',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apprenants.Faculte'),
        ),
        migrations.AddField(
            model_name='cours',
            name='universite',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apprenants.University'),
        ),
    ]
