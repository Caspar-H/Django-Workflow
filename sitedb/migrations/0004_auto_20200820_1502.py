# Generated by Django 3.0.3 on 2020-08-20 05:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sitedb', '0003_siteloginfo_log_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='site',
            name='site_acma_id',
        ),
        migrations.RemoveField(
            model_name='site',
            name='site_cluster',
        ),
        migrations.RemoveField(
            model_name='site',
            name='site_pole_id',
        ),
        migrations.RemoveField(
            model_name='site',
            name='site_pole_owner',
        ),
        migrations.RemoveField(
            model_name='site',
            name='site_rfnsa_id',
        ),
    ]
