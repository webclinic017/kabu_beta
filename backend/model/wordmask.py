from django.db import models

class wordMask(models.Model):
     id        = models.IntegerField(primary_key=True)
     word      =models.CharField(max_length=50, default="")