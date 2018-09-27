from django.db import models

# Create your models here.
class Summary(models.Model):
    title= models.CharField(max_length=1000)
    shortSum = models.CharField(max_length=5000)
    LongSum = models.CharField(max_length=50000)