from django.db import models

class TAGKUBUN(models.Model):
     id       = models.AutoField(primary_key=True)
     name     = models.CharField(max_length=50, default="")

