from django.shortcuts import render
from django.views.generic import DetailView
from front.models import comany,years_data,daily_data
import pandas as pd
from urllib import request
from front.models.daily_data import DailyData

class CompanyDetail(DetailView):
    model               =comany.Company
    queryset            = comany.Company.objects.all()
    template_name       ='company_detail.html'
#     years_data.YearData.objects.all()
    def get_object(self, queryset=None):
        return years_data.YearData.objects.all()


