from django.shortcuts import render
from front.models.daily_data import DailyData
from front.models import settlement_list
from django.http.response import HttpResponse
from front.models.comany import Company
from front.models.years_data import YearData
from statistics import mean
import pandas as pd
from mail.controller.dailysummaryController import dailysummaryController
from backend.controller.doublecontroller.companynews import companynews
from backend.controller.decorate.wordcloud import wordCloud
from front.controller.indicatorcontroller import indicatorController
from front.controller.dailyinfocontroller import dailyInfoController
from django.core.cache import cache

class KabuInfo:
    def homepage(request):
        dailyobj          =DailyData()
        day               =dailyobj.getBasicDay()
        key               ='{0}_homepage'.format(day)
        context           =cache.get(key)
        if context is None:
            result            =dailyobj.getFivedayWeightList();
            basic_company     =dailyobj.getBasicCompany();
            day               =dailyobj.getBasicDay();
            #filter(Q(class_name=class_name[0])| Q(class_name=class_name[1])   )
            context = {
                    'day'           :day.strftime('%Y/%m/%d'),
                    #'class_name'    :class_name,
                    'companylist'   :result,
                    'basic_company' :basic_company
                }
            cache.set(key, context, 60 * 60 *12)

        return render(request, 'homepage.html', context)
    #rise rateが下がる率を表す
    def rise_rate_company(request):
        dailyobj          =DailyData()
        day               =dailyobj.getBasicDay()
        key               ='{0}_rise_rate_company'.format(day)
        result            =cache.get(key)
        if result is None:
            result            =dailyobj.getRisePercentList()
            cache.set(key, result, 60 * 60 *12)

        context={
            'companylist'   :result,
        }
        return render(request, 'rise_rate_company.html', context)


    def getsettlementdata(request):
        settleobj   =settlement_list.Settlement()
        result      =settleobj.getsettlementdata()
        context={
            'companylist'   :result,
        }
        return render(request, 'rise_rate_company.html', context)
    #SR = settle_result  決算結果
    def getsrhomepage(request):
        dailyobj          =DailyData()
        day               =dailyobj.getBasicDay()
        key               ='{0}_getsrhomepage'.format(day)
        result           =cache.get(key)
        if result is None:
            settleobj   =settlement_list.Settlement()
            settle_result   =settleobj.getsettlementdata()


            riserate_result   =dailyobj.getRisePercentList()

            lowlevelresult   =dailyobj.getLowLevelData()

            favoritelist            =dailyobj.getFavoriteCompanylist()['companylist'];
            #print(favoritelist)
            #top price fell rate and is low level 底値圏突入
            result  =[item for item in riserate_result if item['company_code'] in [riseobj['company_code'] for riseobj in lowlevelresult]]
            #A  top price fell rate and is low level 底値圏突入 and
            #  決算　is sunny
            #result      =[item for item in result if item['company_code'] in [reobj['company_code'] for reobj in  settle_result]]
            #B  and fiveweight (should buy?)
            result      =[item for item in result if item['company_code'] in [reobj.company_code for reobj in  favoritelist]]
            cache.set(key, result, 60 * 60 *12)

        context={
            'companylist'   :result,
        }
        return render(request, 'rise_rate_company.html', context)


    def getsettleandsunny(request):
        dailyobj          =DailyData()
        day               =dailyobj.getBasicDay()
        key               ='{0}_getsettleandsunny'.format(day)
        result           =cache.get(key)
        if result is None:
            settleobj   =settlement_list.Settlement()
            settle_result   =settleobj.getsettlementdata()


            riserate_result   =dailyobj.getRisePercentList()

            lowlevelresult   =dailyobj.getLowLevelData()


            #top price fell rate and is low level 底値圏突入
            #
            #result  =[item for item in riserate_result]
            result  =[item for item in riserate_result if item['company_code'] in [riseobj['company_code'] for riseobj in lowlevelresult]]
            #A  top price fell rate and is low level 底値圏突入 and
            #  決算　is sunny
            result      =[item for item in result if item['company_code'] in [reobj['company_code'] for reobj in  settle_result]]
            cache.set(key, result, 60 * 60 *12)
        context={
            'companylist'   :result,
        }
        return render(request, 'rise_rate_company.html', context)

    def getdcflist(request):
        result={}
        def getdcfprice(code):
            yearepslist      =YearData.objects.all().filter(company_code=code)
            yeareps          =[item.year_eps for item in yearepslist]
            price            = mean(yeareps[-2:])*7.5 if len(yeareps)>3 else 0,
            return price[0]
        lastday=DailyData().getBasicDay()
        try:
            for com in Company.objects.filter(monitor_flag=1).order_by('-class_name'):
                current_record = DailyData.objects.filter(day=lastday,company_code=com.company_code).first()
    #             print(current_record)
                if current_record is not None:
                    current_price=current_record.finish_value/10
                    dcfprice=getdcfprice(com.company_code)
                    if dcfprice>current_price:
                        result[dcfprice-current_price]=com
        #                 item ={}
        #                 item['price']=dcfprice-current_price
        #                 item['company']=com
        #                 result.add(item)

        except Exception as e:
            print(e)
        order_result =[]
        for key in sorted(result,reverse=True):
    #         print(key)
    #         print(result[key])
            order_result.append(result[key])

        context={
            'companylist'   :order_result,
        }
        return render(request, 'dcflist.html', context)

    def getDailySummary(request):
        company_num = 10
        dailyobj    = DailyData()
        companylist = dailyobj.getMonitorCompanyList()
        datamatris  = pd.DataFrame(companylist)
        datamatris.eval("""rate = (price_max-price)/price_max""", inplace=True)
        if datamatris.company_code.count()<5 :
            company_num=datamatris.company_code.count()

        datamatris  =datamatris.sort_values("rate",ascending=False)[0:company_num]

        ######################上昇見込み銘柄
        company_codelist=[]
        for item in datamatris['company_code']:
           company_codelist.append(item)

        rate_list=[]
        for item in datamatris['rate']:
            item    =round(float(item),2)*100
            rate_list.append(item)

        companyname_list=[]
        for item in datamatris['company_name']:
            companyname_list.append(item)

        dailysummary={
            'company_codelist'  : company_codelist,
            'rate_list'         : rate_list,
            'companyname_list'  : companyname_list,
        }
        ######################対象銘柄news画像
        companynewsobj      = companynews()
        companylistnews_img =[]
        for company_index in range(company_num):
            companynewsobjtxt               = companynewsobj.getnewstxtViacompanycode(company_codelist[company_index])
            newswcloud_img                  =''
            if len(companynewsobjtxt) >0 :
                wordcloudobj                    =wordCloud()
                newswcloud_img                  =wordcloudobj.word_cloudbase64(companynewsobjtxt)
                companynews_img                 ={
                        'company_code'   :   company_codelist[company_index],
                        'news_img'       :   newswcloud_img,
                        'company_name'   :   companyname_list[company_index],
                }
                companylistnews_img.append(companynews_img)
        ######################vix
        indicatorcontrollerobj                  = indicatorController()
        vix                                     = indicatorcontrollerobj.getVixData()

        japangdp                                = indicatorcontrollerobj.getGDPGraph('japan')
        usagdp                                  = indicatorcontrollerobj.getGDPGraph('united%20states')
        chinagdp                                = indicatorcontrollerobj.getGDPGraph('china')
        ######################PMI
        japanpmiobj                             =indicatorcontrollerobj.getPmi('https://www.investing.com/economic-calendar/ism-manufacturing-pmi-202',202,'Japan')
        japanpmi                                =japanpmiobj['img_str']
        usapmiobj                               =indicatorcontrollerobj.getPmi('https://www.investing.com/economic-calendar/ism-manufacturing-pmi-173',173,'USA')
        usapmi                                  =usapmiobj['img_str']
        chinapmiobj                             =indicatorcontrollerobj.getPmi('https://www.investing.com/economic-calendar/ism-manufacturing-pmi-594',594,'China')
        chinapmi                                =chinapmiobj['img_str']

        japanpmi_data                           =japanpmiobj['data']
        usapmi_data                             =usapmiobj['data']
        chinapmi_data                           =chinapmiobj['data']
        ######################CPI
        japancpiobj                             =indicatorcontrollerobj.getCpi('https://www.investing.com/economic-calendar/national-cpi-992',992,'Japan')
        japancpi                                =japancpiobj['img_str']
        usacpiobj                               =indicatorcontrollerobj.getCpi('https://www.investing.com/economic-calendar/cpi-69',69,'USA')
        usacpi                                  =usacpiobj['img_str']
        chinacpiobj                             =indicatorcontrollerobj.getCpi('https://www.investing.com/economic-calendar/chinese-cpi-743',743,'China')
        chinacpi                                =chinacpiobj['img_str']

        japancpi_data                           = japancpiobj['data']
        usacpi_data                             = usacpiobj['data']
        chinacpi_data                           = chinacpiobj['data']

        conx    ={
            'dailysummary'          :dailysummary,
            'companylistnews_img'   :companylistnews_img,
            'indicator'             :{
                'vix'               :vix,
                'japan_gdp'         :japangdp,
                'usagdp'            :usagdp,
                'china_gdp'         :chinagdp,
                'japanpmi'          :japanpmi,
                'usapmi'            :usapmi,
                'chinapmi'          :chinapmi,

                'japancpi'          :japancpi,
                'usacpi'            :usacpi,
                'chinacpi'          :chinacpi,
                },
            'indicator_data'        :{
                'japanpmi'          :japanpmi_data,
                'usapmi'            :usapmi_data,
                'chinapmi'          :chinapmi_data,

                'japancpi'          :japancpi_data,
                'usacpi'            :usacpi_data,
                'chinacpi'          :chinacpi_data,
                }
        }

        mailControllerobj  =dailysummaryController(conx)
        mailControllerobj.sendMail()

        return HttpResponse('success!')
    def getUnusualAmount(request):
        #getlist
        dailydataobj            = DailyData()
        day                     =DailyData().getBasicDay()
        key                     ='{0}_getUnusualAmount'.format(day)
        company_result          =cache.get(key)
        if company_result is None:
            company_result          =[]
            company_list            =Company.objects.all()
            for company in company_list:
                ave_amount           =dailydataobj.getAveAmount(company.company_code)
                amount               =dailydataobj.getRecentDailyInfo(company.company_code).amount
                #取引量が異常増加して、平均量の10倍になること
                if amount > ave_amount*10:
                    company_result.append(company)
            cache.set(key, company_result, 60 * 60 * 12)
        context={
            'companylist'   :company_result,
        }
        return render(request, 'company_filter/unusual_companylist.html', context)

