# Create your models here.
from django.db import models

class DataPoint(models.Model):
    end_year = models.IntegerField(null=True)
    intensity = models.IntegerField()
    sector = models.CharField(max_length=64, null=True)
    topic = models.CharField(max_length=64, null=True)
    insight = models.CharField(max_length=128, null=True)
    url = models.URLField()
    region = models.CharField(max_length=64, null=True)
    start_year = models.IntegerField(null=True)
    impact = models.IntegerField(null=True)
    added = models.DateTimeField()
    published = models.DateTimeField(null=True)
    country = models.CharField(max_length=128, null=True)
    relevance = models.IntegerField(null=True)
    pestle = models.CharField(max_length=64, null=True)
    source = models.CharField(max_length=64, null=True)
    title = models.CharField(max_length=256, null=True)
    likelihood = models.IntegerField(null=True)
