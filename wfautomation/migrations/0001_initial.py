# Generated by Django 3.0.3 on 2020-09-07 01:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sitedb', '0004_auto_20200820_1502'),
    ]

    operations = [
        migrations.CreateModel(
            name='POIDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poi_1', models.CharField(max_length=300, verbose_name='POI 1')),
                ('poi_2', models.CharField(max_length=300, verbose_name='POI 2')),
                ('poi_3', models.CharField(max_length=300, verbose_name='POI 3')),
                ('poi_4', models.CharField(max_length=300, verbose_name='POI 4')),
                ('poi_5', models.CharField(max_length=300, verbose_name='POI 5')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sitedb.Site')),
            ],
            options={
                'verbose_name': 'POI',
                'verbose_name_plural': 'POI',
                'db_table': 'site_poi',
            },
        ),
    ]