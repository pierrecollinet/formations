# Generated by Django 2.2 on 2019-05-15 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cours', '0009_auto_20190513_1221'),
    ]

    operations = [
        migrations.CreateModel(
            name='SousCategorieCours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cours.Cours')),
                ('sous_categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cours.SousCategorie')),
            ],
        ),
        migrations.DeleteModel(
            name='CategorieCours',
        ),
    ]
