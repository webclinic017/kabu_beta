from django.db import models


class CanSlim(models.Model): 
    #http://markethack.net/archives/51802730.html   
    company_code                = models.ForeignKey('Company', on_delete=models.CASCADE, default=0)
    current_earnings            = models.CharField(max_length=20, default="")
    annual_earnings             = models.CharField(max_length=20, default="")
    new_product_service_flg     = models.CharField(max_length=20, default="")
    supply_and_demand           = models.CharField(max_length=20, default="")
    leader_or_laggard           = models.CharField(max_length=20, default="")
    institutional_sponsorship   = models.CharField(max_length=20, default="")
    market                      = models.CharField(max_length=20, default="")
    
    
    