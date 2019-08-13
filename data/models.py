from django.db import models

# Create your models here.


class ChartData(models.Model):
    name = models.CharField(max_length=10)
    data = models.TextField()


class CoName(models.Model):
    name = models.CharField(max_length=20)





