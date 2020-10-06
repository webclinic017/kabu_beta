from django.db import models

class COMPANY(models.Model):
    code        = models.IntegerField(primary_key=True)
    name        =models.CharField(max_length=50, default="")

