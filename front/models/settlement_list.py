from django.db import models
from front.models.comany import Company
from front.models.daily_data import DailyData
#決算スケジュール
class Settlement(models.Model):
    company_code               =models.ForeignKey('Company', on_delete=models.CASCADE, default=0)
    settle_day                 = models.DateField(max_length=20) 
    
    class Meta:
        unique_together = ("company_code", "settle_day")
        
    def getsettlementdata(self):
        result =[]    
        data            =Settlement.objects.order_by('settle_day')
        for item in data:
            obj={}
            obj['company_code'] =item.company_code.company_code
            obj['company_info'] =Company.objects.filter(company_code=item.company_code.company_code).first()
            obj['settle_day']   =item.settle_day.strftime('%Y/%m/%d')        
            if DailyData.objects.filter(company_code=item.company_code.company_code,kabuyoho_signal='底値圏突入',daily_per__lte=30,daily_per__gte=0.01).count() :
                if obj['company_code'] not in [re['company_code'] for re in result]:
                    result.append(obj)
        return result