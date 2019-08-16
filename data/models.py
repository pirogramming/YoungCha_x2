from django.db import models

# Create your models here.


class ChartData(models.Model):
    name = models.CharField(max_length=10)
    data = models.TextField()


class CoName(models.Model):
    name = models.CharField(max_length=20, primary_key=True)


class CoData(models.Model):
    name = models.ForeignKey(CoName, on_delete=models.CASCADE)
    data = models.TextField()