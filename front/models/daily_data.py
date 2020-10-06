from django.db import models
from front.models.comany import Company
import math
import numpy as np
import pandas as pd
from django.db.models import Max
from django.db.models import F,Value,ExpressionWrapper,fields
from django.db.models.functions import Concat
from decimal import Decimal
from django.db.models import Avg


class DailyData(models.Model):
    company_code        =models.ForeignKey('Company', on_delete=models.CASCADE, default=0)
    day                 = models.DateField(max_length=20)
    start_value         = models.FloatField(max_length=20)
    high_value          = models.FloatField(max_length=20)
    low_value           = models.FloatField(max_length=20)
    finish_value        = models.FloatField(max_length=20)
    amount              = models.FloatField(max_length=20)
    daily_per           =models.FloatField(max_length=20,default=0)
    day_weight          =models.IntegerField(default=0)
    fiveday_weight      =models.IntegerField(default=0)
    buy_signal          =models.IntegerField(default=0)
    sale_signal         =models.IntegerField(default=0)
    kabuyoho_signal     =models.CharField(max_length=20, default=0)

    class Meta:
        unique_together = ("company_code", "day")

    def caldailyweight(self):
        def getnextweight(start_data,next_data):
            if((next_data.finish_value > start_data.finish_value) and (next_data.amount > start_data.amount)):
                return 2
            elif ((next_data.finish_value > start_data.finish_value) and (next_data.amount < start_data.amount)):
                return 1
            elif ((next_data.finish_value < start_data.finish_value) and (next_data.amount > start_data.amount)):
                return -2
            elif ((next_data.finish_value < start_data.finish_value) and (next_data.amount < start_data.amount)):
                return -1
            else:
                return 0

        for companyobj in Company.objects.all():
            info   =DailyData.objects.filter(company_code=companyobj.company_code).order_by('day')
            for i in range(1,len(info)):
                daily_weight    =getnextweight(info[i-1],info[i])
                if info[i].day_weight != daily_weight:
                    info[i].day_weight=daily_weight
                    info[i].save()

    def calfivedailyweight(self):
        def isbuysignal(weightlist):
            buy_signal =0
            fivedayweightlist_plus   = [weightlist[index] for index in range(len(weightlist)) if weightlist[index] > 0]
            threedayweightlist_plus  = [weightlist[index] for index in range(3) if weightlist[index] > 0]
            if len(fivedayweightlist_plus)>3:
                buy_signal = 1
            elif len(threedayweightlist_plus) ==3:
                buy_signal = 1
            else:
                buy_signal=0
            return buy_signal

        def issalesignal(weightlist):
            sale_signal =0
            fivedayweightlist_minus   = [weightlist[index] for index in range(len(weightlist)) if weightlist[index] < 0]
            threedayweightlist_minus  = [weightlist[index] for index in range(3) if weightlist[index] < 0]
            if len(fivedayweightlist_minus)>3:
                sale_signal = 1
            elif len(threedayweightlist_minus) ==3:
                sale_signal = 1
            else:
                sale_signal=0
            return sale_signal

        for companyobj in Company.objects.all():
            info    =DailyData.objects.filter(company_code=companyobj.company_code).order_by('day')
            for i in range(4,len(info)):
                if info[i].fiveday_weight == 0:
                    weightlist    =[
                                info[i].day_weight,
                                info[i-1].day_weight,
                                info[i-2].day_weight,
                                info[i-3].day_weight,
                                info[i-4].day_weight,
                                ]
                    fivedayweight =sum(x for x in weightlist)
                    info[i].fiveday_weight=fivedayweight

                    if isbuysignal(weightlist):
                        info[i].buy_signal=1

                    if issalesignal(weightlist):
                        info[i].sale_signal=1

                    info[i].save()

    #量と価格関係
    def getDailyInfoByStep(self,priceamount_price,priceamount_amount,step):
        start_price         =math.floor(min(priceamount_price)/10)*10
        price_len           =max(priceamount_price)-min(priceamount_price)

        t_round=math.ceil(price_len/10)
        mtx=np.array((priceamount_price,priceamount_amount))
        cmtx=np.transpose(mtx)

        re_mtx={}
        re_mtx['price'] =[]
        re_mtx['amount'] =[]

        start_price_s=start_price

        for i in range(t_round):
            start_price_e   =start_price_s+step
            re_mtx['price'].append(start_price_e)
            re_mtx['amount'].append(sum([item[1] for item in cmtx if ((start_price_s<item[0]) and (item[0]<=start_price_e))]))
            start_price_s   =start_price_e
        return  re_mtx

    def getRisePercentList(self):
        companyobj  =[]
        companyobj  =self.getMonitorCompanyList()


        datamatris  =pd.DataFrame(companyobj)
        datamatris.eval("""rate = (price_max-price)/price_max""", inplace=True)
        datamatris  =datamatris.sort_values("rate",ascending=False)

        datamatris  =datamatris[datamatris['rate']>0.35]
    #     comobj      =Company.objects.in_bulk([item for item in datamatris['company_code']])

    #     print([comobj[item].company_name for item in comobj])
        result =[]
        for item in datamatris['company_code']:
            obj={}
            obj['company_code']=item
            obj['company_info']=Company.objects.filter(company_code=item).first()
            obj['rate']        =round(float(datamatris[datamatris['company_code']==item]['rate']),2)*100
            obj['price']        =round(float(datamatris[datamatris['company_code']==item]['price']),0)/10

            result.append(obj)
        return result

    def getMonitorCompanyList(self):
        companyobj =[]
        lastday=self.getBasicDay()

        for com in Company.objects.filter(monitor_flag=1):
            try:

                if DailyData.objects.filter(day=lastday,company_code=com.company_code).first().amount >2000:
                    companyobj.append({
                        'company_name':com.company_name,
                        'company_code':com.company_code,
                        'price_max':DailyData.objects.filter(company_code=com.company_code).aggregate(Max('finish_value'))['finish_value__max'],
                        'price':DailyData.objects.filter(day=lastday,company_code=com.company_code).first().finish_value
                        })
            except Exception as e:
               continue
        return companyobj

    def getFivedayWeightList(self):
        #class_name  = ['サービス業','情報・通信']
        basic_company   = self.getBasicCompany()
        day             = self.getBasicDay()

        result = DailyData.objects.select_related('company_code').all().values(
                'company_code__company_name',
                'company_code__address',
                'company_code__address_url',
                ).annotate(
                company_code    =F('company_code'),
                company_name    =F('company_code__company_name'),
                feature         =F('company_code__feature'),
                fiveday_weight  =F('fiveday_weight'),
                class_name      =F('company_code__class_name'),
                address         =F('company_code__address'),
                address_url     =F('company_code__address_url'),
                price           =F('finish_value')/10,
                daily_per       =F('daily_per'),
                baisu           =ExpressionWrapper(F('company_code__kabu_sum_number')*Decimal('1.0')*F('finish_value')/(basic_company.kabu_sum_number*basic_company.finish_value), output_field=fields.FloatField()),

                nikkeichart_url       =Concat(Value("https://www.nikkei.com/smartchart/?code="), F('company_code')),
                localchart_url       =Concat(Value("/front/companyinfo/"), F('company_code')),
                ).filter(
                        day=day,buy_signal=1,
                        #daily_per__lte=30,daily_per__gte=0.01,
                    ).order_by('daily_per')
        return result
    def getFavoriteCompanylist(self):
        companylist       =Company.objects.annotate().filter(monitor_flag=1)
        context = {
                'companylist'   :companylist,
            }
        return context
    #基準会社
    @classmethod
    def getBasicCompany(self):
        dailyobj        =DailyData();
        day             =dailyobj.getBasicDay()

        basic_company   =DailyData.objects.select_related('company_code').annotate(
        kabu_sum_number =F('company_code__kabu_sum_number'),
        company_name    =F('company_code__company_name'),
        ).filter(day=day,company_code=7518).first()

        return basic_company

    #基準日
    def getBasicDay(self):
        dailydata       =DailyData.objects.all().values('day').order_by('-day').distinct()
        day             = dailydata[0]['day']
        return day

    def getLowLevelData(self):
        result =[]
        day             = self.getBasicDay()
        data            =DailyData.objects.filter(day=day,kabuyoho_signal='底値圏突入')
        for item in data:
            obj={}
            obj['company_code'] =item.company_code.company_code
            obj['company_info'] =Company.objects.filter(company_code=item.company_code.company_code).first()
            result.append(obj)
        return result
    #株の平均量を取得する
    def getAveAmount(self,code):
        ave_amount  =DailyData.objects.filter(company_code=code).aggregate(Avg('amount'))
        return ave_amount['amount__avg']

    #直近のDaily取引情報
    #return     object        DailyData
    def getRecentDailyInfo(self,code):
        day             = self.getBasicDay()
        data            = DailyData.objects.filter(company_code=code,day=day).first()
        return  data





