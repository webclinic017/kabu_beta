from front.models.daily_data import DailyData
from front.models.years_data import YearData
from django.db.models import Avg
from django.db.models import F,Sum
import pandas as pd

class dailyInfoController:
    #年度財務指標
    def getYearinfo(self,code):
        yearepslist      =YearData.objects.all().filter(company_code=code)
        yeareps          =[item.year_eps for item in yearepslist]
        yearsells        =[item.year_sells for item in yearepslist]
        yearprofits      =[item.year_profits for item in yearepslist]
        year             =[item.year.strftime("%Y/%m/%d") for item in yearepslist]
        companyinfo      ={
            'yeareps'       :yeareps,
            'yearsells'     :yearsells,
            'yearprofits'   :yearprofits,
            'year'          :year,
            }
        return [companyinfo,yeareps]
    #日別での情報
    def getdailyinfo(self,code):
        dailyinfo       =DailyData.objects.all().filter(company_code=code)
        day_info        =[item.day.strftime("%Y/%m/%d") for item in dailyinfo]
        amount          =[item.amount for item in dailyinfo]
        price           =[item.finish_value/10 for item in dailyinfo]
        dailyinfoarr    = {
                'day'       : day_info,
                'amount'    : amount,
                'price'     : price,
            }
        return [dailyinfo,day_info,dailyinfoarr]
    #量と価格
    def getPriceAmount(self,code):
        priceamount                 = DailyData.objects.all().filter(company_code=code).annotate(finishvalue=F('finish_value')).order_by('finishvalue')
        priceamount_amount          =[item.amount for item in priceamount]
        priceamount_price           = [item.finish_value/10 for item in priceamount]

        dailyinfo_priceamount       =DailyData.getDailyInfoByStep('',priceamount_price,priceamount_amount,50)
        d_index                     = dailyinfo_priceamount['amount'].index(max(dailyinfo_priceamount['amount']))
        important_price             =dailyinfo_priceamount['price'][d_index]
        recentpriceobj              =DailyData.objects.all().filter(company_code=code).order_by('-day').first()

        return [dailyinfo_priceamount,important_price,recentpriceobj]
    #月別-量価
    def getMonthAmount(self,dailyinfo):
        pdobj=  pd.DataFrame({
            'day'           : [day.day.strftime("%Y/%m/01") for day in dailyinfo],
            'finish_value'  : [finish_value.finish_value for finish_value in dailyinfo],
            'amount'        : [amount.amount for amount in dailyinfo],
        })
        pdobjresult         = pdobj.groupby('day').mean()


        return [pdobjresult,pdobj]