# Generated by Django 3.0.3 on 2020-11-06 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitedb', '0006_auto_20201030_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteloginfo',
            name='log_datetime_info',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='siteloginfo',
            name='log_major_milestone',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='siteloginfo',
            name='log_operation_type',
            field=models.CharField(default='undefined', max_length=32),
        ),
        migrations.AddField(
            model_name='siteloginfo',
            name='log_sub_milestone',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='siteloginfo',
            name='log_info',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='siteloginfo',
            name='log_site_id',
            field=models.CharField(max_length=16, null=True, verbose_name='log_site_id'),
        ),
    ]
