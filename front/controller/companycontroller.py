from front.models.daily_data import DailyData
from django.shortcuts import render
from front.models.comany import Company
from front.controller.dailyinfocontroller import dailyInfoController
from django.db.models import Avg
from statistics import mean
from backend.controller.doublecontroller.companytag import companyTag
from backend.controller.doublecontroller.companynews import companynews
from backend.controller.decorate.wordcloud import wordCloud
import json
from django.core.cache import cache

class companyController:
    def getFavoriteCompanylist(request):
        dailyobj          =DailyData()
        context           =dailyobj.getFavoriteCompanylist()
        return render(request, 'favorite.html', context)


    #株info
    def getCompanyinfo(request,code):
        dailydataobj            = DailyData()
        day                     =DailyData().getBasicDay()
        key                     ='{0}_Companyinfo_{1}'.format(day,code)

        context                 =cache.get(key)
        if context is None:
            company_name                                            =Company.objects.all().filter(company_code=code).first().company_name
            #年度財務指標
            dailyinfocontrollerobj                                  =dailyInfoController()
            [companyinfo,yeareps]                                   =dailyinfocontrollerobj.getYearinfo(code)
            #日別での情報
            [dailyinfo,day_info,dailyinfoarr]                       =dailyinfocontrollerobj.getdailyinfo(code)
            #量と価格
            [dailyinfo_priceamount,important_price,recentpriceobj]  =dailyinfocontrollerobj.getPriceAmount(code)
            ave_amount                                              =dailyinfo.filter(company_code=code).aggregate(Avg('amount'))

            current_price={
                'important_price'                                   :important_price,
                'recent_price'                                      :recentpriceobj.finish_value/10,
                'recent_buy_signal'                                 :recentpriceobj.buy_signal,
                'recent_sale_signal'                                :recentpriceobj.sale_signal,
                'simple_dcf_price'                                  :mean(yeareps[-2:])*7.5 if len(yeareps)>3 else 0,
            }
            current_amount={
                'ave_amount'        :ave_amount['amount__avg'],
                'recent_amount'     :recentpriceobj.amount,
                'rate'              :round(recentpriceobj.amount/ave_amount['amount__avg'],1),
            }
        #      日別-ウェット
            users_data ={
                'data'              :{
                    'date'          :day_info,
                    'fiveday_weight':[item.fiveday_weight for item in dailyinfo],
                    'day_weight'    :[item.day_weight for item in dailyinfo],
                 },
                'company_info'      :{
                    'company_name'  :company_name,
                    'company_code'  :code,

                    },
                }
        #     月別-量価
            [pdobjresult,pdobj]                 =dailyinfocontrollerobj.getMonthAmount(dailyinfo)
        #     月別-量価
            monthinfo           ={
                'day'           :[day for day in pdobj.day.unique()],
                'price'         :[value/10 for value in pdobjresult.finish_value],
                'amount'        :[amount for amount in pdobjresult.amount],
                }
            #タグ-wordcloud
            companytagobj                       =companyTag()
            taglist                             =companytagobj.gettagListviaCompanycode(code)
            tagwcloud_img                          =""
            if len(taglist)>1:
                wordcloudobj                    =wordCloud()
                taglist                         =','.join(taglist)
                tagwcloud_img                   =wordcloudobj.word_cloud(taglist)

            #news-wordcloud
            companynewsobj                       =companynews()
            newstxt                              =companynewsobj.getnewstxtViacompanycode(code)
            newswcloud_img                       =''
            if len(newstxt) >0 :
                wordcloudobj                    =wordCloud()
                newswcloud_img                  =wordcloudobj.word_cloud(newstxt)

            context ={
                'info'                  : json.dumps(companyinfo),
                'company_name'          : company_name,
                'company_code'          : code,
                'current_price'         : current_price,
                'recent_fiveday_weight' : recentpriceobj.fiveday_weight,
                'monthinfo'             : json.dumps(monthinfo),
                'dailyinfo'             : json.dumps(dailyinfoarr),
                'priceamount'           : json.dumps(dailyinfo_priceamount),
                'users_data'            : json.dumps(users_data),
                'current_amount'        : current_amount,
                'tagwcloud_img'         : tagwcloud_img,
                'newswcloud_img'         : newswcloud_img,
                }
            cache.set(key, context, 60 * 60 * 12)
        return  render(request, 'company_detail.html', context)