# models.py
from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=255)

class Shop(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    shop_type = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag)
