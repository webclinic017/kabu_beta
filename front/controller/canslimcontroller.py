import requests
from front.models.years_data import YearData
from front.models.comany import Company
from django.http.response import HttpResponse
from datetime import datetime as dt
from multiprocessing.dummy import Pool as ThreadPool

class canslimcontroller:
    def getyeardata(self):
        def getwebinfo(company_code):
            #print(company_code)
            url                         = 'https://www.nikkei.com/nkd/company/kessan/?scode={0}&ba=1'.format(company_code);
            r                           = requests.get(url)
            _content                    = r.content
            from bs4 import BeautifulSoup
            soup                        = BeautifulSoup(_content,"html.parser")
            table                       = soup.select('.m-tableType01 table')
            for i in range(len(table[0].select('thead td'))):
                year                    = table[0].select('thead td')[i].text.strip("連").strip("連S").strip("連I").strip("単")
                if(year == '-' or year == '--')         :continue;
                year                    = dt.strptime(year,"%Y/%m")
                sells                   = table[0].select('tr')[1].select('td')[i].text.strip().replace(',', '').replace('－', '-')
                profits                 = table[0].select('tr')[4].select('td')[i].text.strip().replace(',', '').replace('－', '-')
                eps                     = table[0].select('tr')[5].select('td')[i].text.strip().replace(',', '').replace('－', '-')
                if(sells=='-')      :sells=0
                if(profits=='-')    :profits=0
                if(eps=='-')        :eps=0

                companycodeobj            = Company.objects.only('company_code').get(company_code=company_code)
                print(companycodeobj)
                if len(YearData.objects.filter(company_code=companycodeobj,year=year)) ==0:
                    obj =YearData()

                    obj.company_code        = companycodeobj
                    obj.year                = year
                    obj.year_sells          = float(sells)
                    obj.year_profits        = float(profits)
                    obj.year_eps            = float(eps)

                    obj.save()
        year_pool = ThreadPool(4)
        try:
            print('getyeardata start!')
            results = year_pool.map(getwebinfo,Company.objects.all())
        except Exception as e:
            print(e)
        year_pool.close()
        print('hello')
        return HttpResponse('hello')

