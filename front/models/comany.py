from django.db import models


class Company(models.Model):    
    company_code            =models.CharField(max_length=50, primary_key=True)
    company_name            =models.CharField(max_length=50, default="")
    address                 =models.CharField(max_length=50, default=0)
    address_url             =models.CharField(max_length=100, default=0)
    chart_url               =models.CharField(max_length=50, default=0)
    feature                 =models.CharField(max_length=150, default=0)
    related_bussiness       =models.CharField(max_length=50, default=0)
    tel                     =models.CharField(max_length=50, default=0)
    class_name              =models.CharField(max_length=20, default=0)
    company_name_english    =models.CharField(max_length=20, default=0)
    represent_ceo           =models.CharField(max_length=20, default=0)
    built_date              =models.CharField(max_length=20, default=0)
    market_name             =models.CharField(max_length=20, default=0)
    on_market_date          =models.CharField(max_length=20, default=0)
    final_date              =models.CharField(max_length=50, default=0)
    unit_kabu               =models.CharField(max_length=20, default=0)
    employee_num            =models.CharField(max_length=20, default=0)
    employee_age            =models.CharField(max_length=20, default=0)
    employee_salary         =models.CharField(max_length=20, default=0)
    monitor_flag            =models.IntegerField( default=0)
    kabu_sum_number         =models.IntegerField( default=0)
    
    
                
        
        
    
    
    