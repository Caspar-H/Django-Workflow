from django.db import models
from django.urls import reverse
from django.utils import timezone


# Create your models here.
class Site(models.Model):
    site_id = models.CharField(max_length=16, unique=True, verbose_name='TPG Site ID')
    site_name = models.CharField(max_length=64, unique=True, verbose_name='TPG Site Name')
    site_vha_id = models.CharField(max_length=16, unique=True, null=True, verbose_name='VHA Site ID')
    site_vha_name = models.CharField(max_length=64, unique=True, null=True, verbose_name='VHA Site Name')
    site_lat = models.FloatField(verbose_name='Latitude')
    site_long = models.FloatField(verbose_name='Longitude')
    site_state = models.CharField(max_length=32, verbose_name='State')
    site_pole_id = models.CharField(max_length=64, null=True, verbose_name='Pole ID')
    site_rfnsa_id = models.CharField(max_length=12, unique=True, null=True, verbose_name='RFNSA ID')
    site_acma_id = models.CharField(max_length=12, unique=True, null=True, verbose_name='ACMA ID')
    site_pole_owner = models.CharField(max_length=64, null=True, verbose_name='Pole Owner')

    def __str__(self):
        return self.site_id

    def get_absolute_url(self):
        return reverse('sitedb:site_detail_info', args=[self.site_id])

    class Meta:
        verbose_name = 'SiteBasicData'
        verbose_name_plural = 'SiteBasicData'
        ordering = ['site_id']
        db_table = 'site_basic'


class SiteActivation(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE, related_name='site_activation')
    activation_plan = models.BooleanField(default=False, verbose_name='Activation Plan')
    activation_schedule = models.CharField(max_length=32, verbose_name='Activation Schedule')
    activation_status = models.CharField(max_length=32, verbose_name='Activation Status')


class SiteSwap(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE, related_name='site_swap')
    swap_plan = models.BooleanField(default=False, verbose_name='Swap Plan')
    swap_schedule = models.CharField(max_length=32, verbose_name='Swap Schedule')
    swap_status = models.CharField(max_length=32, verbose_name='Swap Status')


class SiteLogInfo(models.Model):
    log_site_id = models.CharField(max_length=16, null=True, verbose_name='log_site_id')

    log_created = models.DateTimeField(editable=False)
    log_modified = models.DateTimeField()

    # if log_datetime_info is null, datetime info is collected from log_created/modified.
    # it is used in early stage when some of milestone info cannot be updated in time.
    log_datetime_info = models.DateTimeField(null=True)

    log_info = models.CharField(max_length=128, null=True)
    log_user = models.CharField(max_length=64, verbose_name='log_user', default='None')

    log_major_milestone = models.CharField(max_length=64, null=True)
    log_sub_milestone = models.CharField(max_length=128, null=True)

    # operation type
    # 1. single_claim, single_complete, single_assign,
    # 2. batch_claim, batch_complete,
    # 3. workflow_newsite_initialization, workflow_status_mapping,
    # 4. data_newsite_initialization, data_status_mapping,
    log_operation_type = models.CharField(max_length=32, default='undefined')

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.log_created = timezone.now()
        self.log_modified = timezone.now()
        return super(SiteLogInfo, self).save(*args, **kwargs)

    class Meta:
        db_table = 'site_log_info'
        ordering = ['-log_created']
