from django.db import models

# Create your models here.


class CodeData(models.Model):
    code = models.CharField(max_length=6)
    aggregate_value_t = models.IntegerField()
    aggregate_value_y = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



# class User(models.Model):
#     name = models.CharField(max_length=30)
#     cellphone=models.CharField(max_length=100)
#     address= models.CharField(max_length=100)
#     email=models.CharField(max_length=100)
#     birthday=models.IntegralField(max_length=10)
#     def __str__(self):
#         return self.name