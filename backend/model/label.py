from django.db import models

class LABEL(models.Model):
    label_id        =models.IntegerField(primary_key=True)
    label_name     = models.CharField(max_length=50, default="")
