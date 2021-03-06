# Generated by Django 2.2 on 2019-05-17 16:45

from django.db import migrations, models
import django.db.models.deletion
import partenaires.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SalleCours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
                ('nom_abreviation', models.CharField(blank=True, max_length=200, null=True)),
                ('adresse', models.CharField(max_length=200)),
                ('telephone', models.CharField(max_length=200)),
                ('capacite_maximale', models.SmallIntegerField(blank=True, null=True)),
                ('lat', models.CharField(blank=True, max_length=200, null=True)),
                ('long', models.CharField(blank=True, max_length=200, null=True)),
                ('rue', models.CharField(blank=True, max_length=200, null=True)),
                ('numero', models.CharField(blank=True, max_length=200, null=True)),
                ('code_postal', models.CharField(blank=True, max_length=200, null=True)),
                ('ville', models.CharField(blank=True, max_length=200, null=True)),
                ('plan_acces', models.ImageField(blank=True, null=True, upload_to='mes_images/')),
            ],
        ),
        migrations.CreateModel(
            name='SalleCoursImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=partenaires.models.image_upload_to)),
                ('salle_cours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partenaires.SalleCours')),
            ],
        ),
    ]
