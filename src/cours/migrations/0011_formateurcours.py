# Generated by Django 2.2 on 2019-05-18 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('formateurs', '0004_formateur_active'),
        ('cours', '0010_auto_20190515_1242'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormateurCours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cours.Cours')),
                ('formateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formateurs.Formateur')),
            ],
        ),
    ]
