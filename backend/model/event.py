from django.db import models
from django.utils import timezone

class EVENT(models.Model):
    name        =models.CharField(max_length=50, default="")
    start_date  =models.DateField(default=timezone.now)
    end_date    =models.DateField(default=timezone.now)
    del_flg     = models.IntegerField(default=0)
