from django.db import models
from django.urls import reverse
from django.utils import timezone


# Create your models here.
class Site(models.Model):
    site_id = models.CharField(max_length=16, unique=True, verbose_name='Site ID')
    site_name = models.CharField(max_length=64, unique=True, verbose_name='Site Name')
    site_lat = models.FloatField(verbose_name='Latitude')
    site_long = models.FloatField(verbose_name='Longitude')
    # site_cluster = models.CharField(max_length=64, verbose_name="Cluster")
    site_state = models.CharField(max_length=32, verbose_name='State')
    # site_pole_owner = models.CharField(max_length=64, verbose_name='Pole Owner')
    # site_pole_id = models.CharField(max_length=64, verbose_name='Pole ID')
    # site_rfnsa_id = models.CharField(max_length=12, unique=True, null=True, verbose_name='RFNSA ID')
    # site_acma_id = models.CharField(max_length=12, unique=True, null=True, verbose_name='ACMA ID')

    def __str__(self):
        return self.site_id

    def get_absolute_url(self):
        return reverse('sitedb:site_detail_info', args=[self.site_id])

    class Meta:
        verbose_name = 'SiteBasicData'
        verbose_name_plural = 'SiteBasicData'
        ordering = ['site_id']
        db_table = 'site_basic'


class SiteLogInfo(models.Model):
    log_site_id = models.CharField(max_length=16, verbose_name='log_site_id')

    log_created = models.DateTimeField(editable=False)
    log_modified = models.DateTimeField()

    log_info = models.CharField(max_length=128)
    log_user = models.CharField(max_length=64, verbose_name='log_user', default='None')

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.log_created = timezone.now()
        self.log_modified = timezone.now()
        return super(SiteLogInfo, self).save(*args, **kwargs)

    class Meta:
        db_table = 'site_log_info'
        ordering = ['-log_created']
