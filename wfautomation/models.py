from django.db import models

# Create your models here.
from sitedb.models import Site


class POIDescription(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    poi_1 = models.CharField(max_length=300, verbose_name="POI 1")
    poi_2 = models.CharField(max_length=300, verbose_name="POI 2", null=True)
    poi_3 = models.CharField(max_length=300, verbose_name="POI 3", null=True)
    poi_4 = models.CharField(max_length=300, verbose_name="POI 4", null=True)
    poi_5 = models.CharField(max_length=300, verbose_name="POI 5", null=True)

    class Meta:
        verbose_name = 'POI'
        verbose_name_plural = 'POI'
        db_table = 'site_poi'


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'site_{0}/{1}'.format(instance.site_id, filename)


class SiteSurveyDocuments(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    poi_1_description = models.CharField(max_length=300, blank=True, null=True)
    poi_1_measurement = models.FloatField(default=0, blank=True, null=True)
    poi_1_document = models.FileField(upload_to=user_directory_path)

    poi_2_description = models.CharField(max_length=300, blank=True, null=True)
    poi_2_measurement = models.FloatField(default=0, blank=True, null=True)
    poi_2_document = models.FileField(upload_to=user_directory_path)

    poi_3_description = models.CharField(max_length=300, blank=True, null=True)
    poi_3_measurement = models.FloatField(default=0, blank=True, null=True)
    poi_3_document = models.FileField(upload_to=user_directory_path)

    poi_4_description = models.CharField(max_length=300, blank=True, null=True)
    poi_4_measurement = models.FloatField(default=0, blank=True, null=True)
    poi_4_document = models.FileField(upload_to=user_directory_path)

    poi_5_description = models.CharField(max_length=300, blank=True, null=True)
    poi_5_measurement = models.FloatField(default=0, blank=True, null=True)
    poi_5_document = models.FileField(upload_to=user_directory_path)

    uploaded_at = models.DateTimeField(auto_now_add=True)
