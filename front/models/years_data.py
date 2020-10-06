from django.db import models
from front.models.comany import Company

class YearData(models.Model):
    company_code                = models.ForeignKey('Company', on_delete=models.CASCADE, default=0)
    year                        = models.DateField(max_length=20, default="")
    year_sells                  = models.FloatField(default=0)
    year_profits                = models.FloatField(default=0)
    year_eps                    = models.FloatField(default=0)
    
    class Meta:
        unique_together = ("company_code", "year")
   
    
    