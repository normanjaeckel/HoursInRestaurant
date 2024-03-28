# Generated by Django 5.0.3 on 2024-03-28 00:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=255, verbose_name='Nachname')),
                ('first_name', models.CharField(max_length=255, verbose_name='Vorname')),
            ],
            options={
                'verbose_name': 'Arbeitnehmer/in',
                'verbose_name_plural': 'Arbeitnehmer/innen',
            },
        ),
        migrations.CreateModel(
            name='Volume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Bezeichnung')),
            ],
            options={
                'verbose_name': 'Aktenband',
                'verbose_name_plural': 'Aktenbände',
            },
        ),
        migrations.CreateModel(
            name='Sheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.CharField(max_length=255, verbose_name='Seite')),
                ('date', models.DateField(verbose_name='Datum')),
                ('begin', models.TimeField(verbose_name='Beginn der Arbeitszeit')),
                ('end', models.TimeField(verbose_name='Ende der Arbeitszeit')),
                ('break_time', models.PositiveIntegerField(verbose_name='Pause (in Minuten)')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hoursinrestaurant.employee')),
                ('volume', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hoursinrestaurant.volume')),
            ],
            options={
                'verbose_name': 'Stundenzettel',
                'verbose_name_plural': 'Stundenzettel',
            },
        ),
    ]
