# Generated by Django 2.2 on 2019-08-05 10:15

from django.db import migrations, models
import django.db.models.deletion
import fontawesome.fields


class Migration(migrations.Migration):

    dependencies = [
        ('formations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategorieFaq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categorie', models.CharField(blank=True, max_length=200, null=True)),
                ('icon', fontawesome.fields.IconField(blank=True, max_length=60, null=True)),
                ('slug', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Encouragement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proverbe', models.TextField()),
                ('auteur', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='faq',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='formations.CategorieFaq'),
        ),
    ]
