from django.db import models

# Create your models here.

class AllHouse(models.Model):
    title = models.CharField(max_length=255,null=True)
    village = models.CharField(max_length=255, null=True)
    are = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, null=True)
    size = models.CharField(max_length=255, null=True)
    ori = models.CharField(max_length=255, null=True)
    info = models.CharField(max_length=255, null=True)
    rent = models.CharField(max_length=255, null=True)
    people = models.CharField(max_length=255, null=True)
    dist = models.CharField(max_length=255, null=True)

