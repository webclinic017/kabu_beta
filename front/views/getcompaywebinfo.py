from django.http.response import HttpResponse
import requests,urllib
import front.models.comany as comany
import front.models.canslim as canslim
import front.models.daily_data as daily_data
from selenium import webdriver
from lxml import html
from urllib import request
import re
import os
from front.models import settlement_list
from datetime import datetime as dt
from front.models.returnformat import ReturnFormtat
from multiprocessing.dummy import Pool as ThreadPool
from front.models.canslim import CanSlim
from selenium.webdriver.chrome.options import Options
import traceback
from front.controller.canslimcontroller import canslimcontroller

path =os.path.abspath(__file__)+'/../../../chromedriver'
class CompanyInfo:

    def getnik225(self):
        url                         = 'https://nik225.sakura.ne.jp/index.html';
        r                           = requests.get(url)
        _content                    = r.content
        from bs4 import BeautifulSoup
        soup                        = BeautifulSoup(_content,"html.parser")
        conpanylist                 = soup.select('#hpb-main tr')
        for comp in conpanylist:
            company_code            = comp.select('td,th')[1].text.strip()
            objcompany              =CompanyInfo()
            objcompany.getnikinfo(company_code)
        return HttpResponse('success')
    def getnikinfo(self,code):
        company_code    =int(code)

        if comany.Company.objects.filter(company_code=company_code).count() ==0:
            try:
                info                        = {}
                yahoo_info                  = get_yahoocompany_info(company_code)

                info['address']             = yahoo_info['address'].strip(),
                info['address_url']         = yahoo_info['address_url'].strip(),
                info['related_bussiness']   = yahoo_info['related_bussiness'].strip()
                info['company_name_english']   = yahoo_info['company_name_english'].strip()

                companyobj                         =comany.Company()
                companyobj.company_name            = yahoo_info['company_name']
                companyobj.company_code            =   company_code
                companyobj.address                 =   info['address'][0][0:40]
                companyobj.address_url             =   info['address_url'][0][:30]
                companyobj.chart_url               =   ""
                companyobj.feature                 =   yahoo_info['feature'].strip()
                companyobj.related_bussiness       =   info['related_bussiness'][0][0:40]
                companyobj.tel                     =   yahoo_info['tel'].strip()
                companyobj.class_name              =   yahoo_info['class_name'].strip()
                companyobj.company_name_english    =   info['company_name_english'][0][0:40]
                companyobj.represent_ceo           =   yahoo_info['represent_ceo'].strip()
                companyobj.built_date              =   yahoo_info['built_date'].strip()
                companyobj.market_name             =   yahoo_info['market_name'].strip()
                companyobj.on_market_date          =   yahoo_info['on_market_date'].strip()
                companyobj.final_date              =   yahoo_info['final_date'].strip()
                companyobj.unit_kabu               =   yahoo_info['unit_kabu'].strip()
                companyobj.employee_num            =   yahoo_info['employee_num'].strip()
                companyobj.employee_age            =   yahoo_info['employee_age'].strip()
                companyobj.employee_salary         =   yahoo_info['employee_salary'].strip()
                companyobj.monitor_flag            =   0
    #             companyobj.kabu_sum_number         =getkabusumnumber(code)

                companyobj.save()
            except Exception as err:
                traceback.print_tb(err.__traceback__)
                print('nothing')
                #nothing
            return HttpResponse('success')
        else:
            return HttpResponse('fail!すでに存在していますから')

    def getdailyinfostack(request):
        obj         =CompanyInfo()
        cansimobj   =canslimcontroller()
        obj.getdailyinfo()
        obj.getdailyper()
        obj.calcuteweight()
        obj.calcutefiveweight()
        obj.deleteotherData()
        cansimobj.getyeardata()
        return HttpResponse('getdailyper,calcuteweight,calcutefiveweight success')

    def getdailyinfo(self):
        import datetime
        print('決算情報を取る　start!')
        for _day in range(1,55):
            daysafter   = datetime.date.today() + datetime.timedelta(days=_day)
            _str         ='{0}{1}{2}'.format(daysafter.year,daysafter.month,daysafter.day if len(str(daysafter.day))>1 else "0"+str(daysafter.day))
        print('決算情報を取る　end!')
        print('get daily price start!')

        def getdailyinfobycode(company):
                url                 = "https://kabutan.jp/stock/read?c={0}&m=1&k=1".format(company.company_code)
                print(url)
                try:
                    webcontent      = urllib.request.urlopen(url,timeout=10)
                    kabuinfo        = webcontent.read().decode('utf-8');
                    line_array      =kabuinfo.splitlines(True)

                    print(company)
                    try:
                        if len(line_array)>7:
                            for i in range(1, len(line_array)):
                                dailydata = line_array[i]
                                info = dailydata.split(',')
                                company_code        = comany.Company.objects.only('company_code').get(company_code=company.company_code)
                                day                 = dt.strptime(re.sub(r'#.*',"",info[0]),"%Y.%m.%d")
                                if len(daily_data.DailyData.objects.filter(company_code=company_code,day=day)) ==0:
                                    obj  = daily_data.DailyData()
                                    obj.company_code    = company_code
                                    obj.day             =day
                                    obj.start_value     =info[1]
                                    obj.high_value      =info[2]
                                    obj.low_value       =info[3]
                                    obj.finish_value    =info[4]
                                    obj.amount          =info[5]

                                    obj.save()
                    except urllib.error.HTTPError as e:
                        print('getdailyiperbycode 7')
                        print(e.code)
                except Exception as e:
                    print('getdailyinfobycode')
                    print(e)


        for company in comany.Company.objects.all():
            try:
                getdailyinfobycode(company)
            except Exception as e:
                print(e)
                continue

        print('get daily price finished!')
        return

    def getdailyper(self):
        print('get daily per start!')
        def getdailyiperbycode(company):
            try:
                obj              =daily_data.DailyData.objects.all().filter(company_code=company.company_code,).order_by('-day').first()
                url              ='https://kabutan.jp/stock/?code=' + company.company_code
                print(url)
                r                = requests.get(url,timeout=10)
                _content         = r.content
                from bs4 import BeautifulSoup
                soup             = BeautifulSoup(_content,"html.parser")
                pertxt           =soup.select('#stockinfo_i3 tr td')[0].text.strip('倍')
                if pertxt == '－':pertxt=0
                obj.daily_per    =pertxt
                obj.kabuyoho_signal         =getkabuyohosignal(company.company_code)
                obj.save()
            except Exception as e:
                print('getdailyiperbycode')
                print(e)

        #threa
        dailyper_pool = ThreadPool(4)
        try:
            dailyper_pool.map(getdailyiperbycode,comany.Company.objects.all())
        except Exception as e:
            print(e)
        dailyper_pool.close()


        print('get daily per finished!')
        #driver.quit()
        return

    def calcuteweight(self):
        print('daily weight calculate start!')
        daily_data.DailyData.caldailyweight(self)
        print('daily weight calculate finished!')
        return
    def calcutefiveweight(self):
        print('five day weight calculate start!')
        daily_data.DailyData.calfivedailyweight(self)
        print('five day weight calculate finished!')

        return

    def deleteotherData(self):
        dailyobj=daily_data.DailyData()
        print('delete other data start!')
        company_codelist= daily_data.DailyData.objects.values_list('company_code', flat=True).filter(day=dailyobj.getBasicDay()).distinct()
        comany.Company.objects.exclude(company_code__in=company_codelist).delete()
        settlement_list.Settlement.objects.filter(settle_day__lte=dailyobj.getBasicDay()).delete()
        print('delete other data finished!')
        return

    def getkabusumnumber(self):
        result = getkabusumnumber(9412)
        return HttpResponse(result)
    def addtofavorite(self,code):
        company_code    =int(code)
        companyobj = comany.Company.objects.get(company_code=company_code)

        try:
            companyobj.monitor_flag=1
            companyobj.save()
            result = ReturnFormtat.successinonfo()
        except:
            result = ReturnFormtat.failinfo()

        return HttpResponse(result.message)
    #
    def removefavorite(self,code):
        company_code    =int(code)
        companyobj = comany.Company.objects.get(company_code=company_code)

        try:
            companyobj.monitor_flag=0
            companyobj.save()
            result = ReturnFormtat.successinonfo()
        except:
            result = ReturnFormtat.failinfo()

        return HttpResponse(result.message)

    def savemapimage(self):
        options     = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--user-data-dir=/tmp/selenium")
        path        ='/usr/local/bin/chromedriver'
        dirve       = webdriver.Chrome(path,chrome_options=options)
        for com in comany.Company.objects.filter(company_code__gt='8058'):
            url         = "https://www.google.com/maps/search/?api=1&query={0}&zoom=21".format(com.address)
            filename    = os.path.join(os.getcwd(), "maps/{0}{1}.png".format(com.company_code,com.company_name))
            print(filename)
            dirve.set_window_size(1280, 720)
            dirve.get(url)
            dirve.save_screenshot(filename)

        dirve.quit()
        return HttpResponse('success')


def get_yahoocompany_info(code):
        try:
            url='https://profile.yahoo.co.jp/fundamental/?s=' + str(code)
            r                           = requests.get(url,timeout=10)
            _content                    = r.content
            from bs4 import BeautifulSoup
            soup                        =BeautifulSoup(_content,"html.parser")

            conpanylist                 =soup.select('table')
            obj1={}

            obj1= {
                'company_name'          : ''.join(soup.select('.selectFinTitle h1')[0].text),
                'address'               : str(conpanylist[3].select('td td')[5].text.strip('  [周辺地図]')),
                'address_url'           : str(conpanylist[3].select('td td')[5].select('a')[0].attrs['href']),
                'feature'               : conpanylist[3].select('td td')[1].text if (conpanylist[3].select('td td')[0].text == '特色') else "",
                'related_bussiness'     : conpanylist[3].select('td td')[3].text if (conpanylist[3].select('td td')[2].text == '連結事業') else "",
                'tel'                   : conpanylist[3].select('td td')[9].text if (conpanylist[3].select('td td')[8].text == '電話番号') else "",
                'class_name'            : conpanylist[3].select('td td')[11].text if (conpanylist[3].select('td td')[10].text == '業種分類') else "",
                'company_name_english'  : conpanylist[3].select('td td')[13].text if (conpanylist[3].select('td td')[12].text == '英文社名') else "",
                'represent_ceo'         : conpanylist[3].select('td td')[15].text if (conpanylist[3].select('td td')[14].text == '代表者名') else "",
                'built_date'            : conpanylist[3].select('td td')[17].text if (conpanylist[3].select('td td')[16].text == '設立年月日') else "",
                'market_name'           : conpanylist[3].select('td td')[19].text if (conpanylist[3].select('td td')[18].text == '市場名') else "",
                'on_market_date'        : conpanylist[3].select('td td')[21].text if (conpanylist[3].select('td td')[20].text == '上場年月日') else "",
                'final_date'            : conpanylist[3].select('td td')[23].text if (conpanylist[3].select('td td')[22].text == '決算') else "",
                'unit_kabu'             : conpanylist[3].select('td td')[25].text if (conpanylist[3].select('td td')[24].text == '単元株数') else "",
                'employee_num'          : conpanylist[3].select('td td')[27].text if (conpanylist[3].select('td td')[26].text == '従業員数（単独）') else "",
                'employee_age'          : conpanylist[3].select('td td')[31].text if (conpanylist[3].select('td td')[30].text == '平均年齢') else "",
                'employee_salary'       : conpanylist[3].select('td td')[33].text if (conpanylist[3].select('td td')[32].text == '平均年収') else "",
                }
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            print('get company info error')
        return obj1;
#総合株数を取得する
def getkabusumnumber(code):
    url         = "https://www.nikkei.com/nkd/company/gaiyo/?scode={0}&ba=1".format(code)

    data        = request.urlopen(url)
    raw_html    = data.read().decode("utf-8")
    _html       = html.fromstring(str(raw_html))
    _content    = _html.xpath('//*[@id="basicInformation"]/div/div[2]/div/div/table/tbody/tr[15]/td')
    result      = int(_content[0].text.strip('\\r\\n').strip().strip('\\r\\n').replace(',','').replace('(株)',''))
    return result

def getkabuyohosignal(code):
    #driver = webdriver.Chrome(path)
    url         = "https://kabuyoho.ifis.co.jp/index.php?action=tp1&sa=report_ts&bcode={0}#tran".format(code)
    #driver.get(url)
    r                           = requests.get(url,timeout=10)
    _content                    = r.content
    from bs4 import BeautifulSoup
    soup                        = BeautifulSoup(_content,"html.parser")
    result                      =soup.select('.cont_figu td')[3].text.strip()
    print(result)
    #driver.quit()
    return result

def getschedule(req,_day):

    try:
        for i in [1,2,3]:
            print(_day)
            url                 = "https://kabuyoho.ifis.co.jp/index.php?action=tp1&&sa=schedule&ym={0}&lst={1}&srt=pd&pageID={2}".format(_day[:6],_day,i)
            print(url)
            r                           = requests.get(url)
            _content                    = r.content
            from bs4 import BeautifulSoup
            soup                        = BeautifulSoup(_content,"html.parser")
            tr                       = soup.select('#progress_list table tr')[1:]
            codelist    =[node.select('td a')[0].text for node in tr if node.select('td')[3].select('p.mr')[0]>70]
            print(codelist)
            for code in codelist:
                CompanyInfo.getnikinfo('',code)
                obj                 =settlement_list.Settlement()
                obj.company_code    =comany.Company.objects.only('company_code').get(company_code=code)
                obj.settle_day      =dt.strptime(_day, '%Y%m%d')
                seobj=settlement_list.Settlement.objects.filter(company_code=obj.company_code,settle_day=obj.settle_day )
                if len(seobj)==0:
                    obj.save()
    except:
        print('except')
    return  HttpResponse('success')


def importtokyoone(self):
    import bs4
    for i in range(43):
        url ="http://www.jpubb.com/list/list.php?listed=1&se=tou1&pageID={}".format(i+1)
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        for a in soup.select('.code a'):
            company_url="http://127.0.0.1:8000/front/getnik/"+a.text
            if len(a.text):
                CompanyInfo.getnikinfo(self,a.text)
            print(company_url)

#import kabu code into DB via txt list
def importKabucodeViaTxt(request):
    txt_address = os.path.dirname(__file__) + '/../../codelist/code.txt'
    code_list =[]
    with open(txt_address,'r') as file:
        for i in file:
            a =i.strip('\n')
            code_list.append(a)

    for code in code_list:
        print(code)
        company_url=request.META['HTTP_HOST'] + "/front/getnik/"+(code)

        CompanyInfo.getnikinfo('',code)

    return 'success'



