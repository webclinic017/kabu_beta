from urllib import request
import pandas as pd
from django.shortcuts import render
import urllib.request,json
import requests,urllib
from bs4 import BeautifulSoup
from front.decorate.linegraphcontroller import lineGraphController
from front.controller.bearerauth import BearerAuth
class indicatorController:
    #liyang indicator
    def getnikeiindex(req):
        indicatorobj        =indicatorController()
        url                 = "https://kabutan.jp/stock/read?c=0000&m=1&k=1"
        webcontent          = request.urlopen(url)
        data                = str(webcontent.read().decode('utf-8'));
        dailyinfo           = pd.Series(data.split('\n'))[1:-1]
        dailyinfo           =[row.split(',') for row in dailyinfo]
        data1               =pd.DataFrame(dailyinfo,columns=['day', 'start_price', 'high_price','low_price','finish_price','amount','row7','row8','row9','row10','row11','row12','row13','row14','row15','row16'])

        result={}

        result['date']         =list(reversed(list(data1['day'].values)))
        result['finish_price'] =list(reversed(list(data1['finish_price'].values)))
        result['amount']       =list(reversed(list(data1['amount'].values)))

        thirtyday_price     =indicatorobj.getMa(result['finish_price'],30)
        seventyday_price    =indicatorobj.getMa(result['finish_price'],72)

        def getthirtydayseventyday_ave(thirtyday_price,seventyday_price):
            result=[]
            for i in range(len(seventyday_price)):
                if seventyday_price[i] == 0:
                    result.append(0)
                else:
                    ave=(seventyday_price[i] +thirtyday_price[i])/2
                    result.append(ave)
            return result
        context={
              'date'                :result['date'],
               'finish_price'       :result['finish_price'],
              'amount'              :result['amount'],
              '30day_price'         :thirtyday_price,
              '72day_price'         :seventyday_price,
              'liyang_price'        :getthirtydayseventyday_ave(thirtyday_price,seventyday_price),
              'liyang_price_upper'  :[item*1.1 for item in getthirtydayseventyday_ave(thirtyday_price,seventyday_price)],
              'liyang_price_down'   :[item*0.9 for item in getthirtydayseventyday_ave(thirtyday_price,seventyday_price)],
            }
        return  render(req, 'indicator/nikeiindex.html', context)
    def getMa(self,price_value,step):
        mylist = price_value
        N = step
        cumsum, moving_aves = [0], []

        for i, x in enumerate(mylist, 1):
            cumsum.append(cumsum[i-1] + int(x))
            if i>=N:
                moving_ave = (cumsum[i] - cumsum[i-N])/N
                moving_aves.append((moving_ave))
            else:
                moving_aves.append(0)
        return moving_aves
    #vix
    def getVixData(self):
        data                =''
        url                 = "https://scanner.tradingview.com/cfd/scan"
        method = "POST"
        obj = {"symbols":{"tickers":["TVC:VIX"],"query":{"types":[]}},
               "columns":["Recommend.Other","Recommend.All","Recommend.MA","RSI","RSI[1]","Stoch.K","Stoch.D","Stoch.K[1]","Stoch.D[1]","CCI20","CCI20[1]","ADX","ADX+DI","ADX-DI","ADX+DI[1]","ADX-DI[1]","AO","AO[1]","Mom","Mom[1]","MACD.macd","MACD.signal","Rec.Stoch.RSI","Stoch.RSI.K","Rec.WR","W.R","Rec.BBPower","BBPower","Rec.UO","UO","EMA5","close","SMA5","EMA10","SMA10","EMA20","SMA20","EMA30","SMA30","EMA50","SMA50","EMA100","SMA100","EMA200","SMA200","Rec.Ichimoku","Ichimoku.BLine","Rec.VWMA","VWMA","Rec.HullMA9","HullMA9","Pivot.M.Classic.S3","Pivot.M.Classic.S2","Pivot.M.Classic.S1","Pivot.M.Classic.Middle","Pivot.M.Classic.R1","Pivot.M.Classic.R2","Pivot.M.Classic.R3","Pivot.M.Fibonacci.S3","Pivot.M.Fibonacci.S2","Pivot.M.Fibonacci.S1","Pivot.M.Fibonacci.Middle","Pivot.M.Fibonacci.R1","Pivot.M.Fibonacci.R2","Pivot.M.Fibonacci.R3","Pivot.M.Camarilla.S3","Pivot.M.Camarilla.S2","Pivot.M.Camarilla.S1","Pivot.M.Camarilla.Middle","Pivot.M.Camarilla.R1","Pivot.M.Camarilla.R2","Pivot.M.Camarilla.R3","Pivot.M.Woodie.S3","Pivot.M.Woodie.S2","Pivot.M.Woodie.S1","Pivot.M.Woodie.Middle","Pivot.M.Woodie.R1","Pivot.M.Woodie.R2","Pivot.M.Woodie.R3","Pivot.M.Demark.S1","Pivot.M.Demark.Middle","Pivot.M.Demark.R1"]}
        json_data = json.dumps(obj).encode("utf-8")
        headers = {"Content-Type" : "application/json"}

        request             = urllib.request.Request(url, data=json_data, headers=headers, method=method)
        result              =0
        with urllib.request.urlopen(request) as response:
            response_body   = response.read().decode("utf-8")
            result_objs     = json.loads(response_body)
            result          =result_objs['data'][0]['d'][31]
            response.close()
        return result
    #GDP
    def getGDPGraph(self,country):
        data    =''
        url                 ='https://api.tradingeconomics.com/historical/country/{0}/indicator/gdp?c=guest:guest&format=json'.format(country)
        webcontent          = request.urlopen(url)
        data                = webcontent.read().decode('utf-8')
        df                  = pd.read_json(data)
        lastupdatearr       = [item[:10] for item in df.LastUpdate]

        linegraphobj        = lineGraphController('{0} GDP'.format(country),'日付','value')
        str                 = linegraphobj.getBase64LineChart(lastupdatearr, df.Value)
        return str

    #PM!
    def getPmi(self,url,key,country):
        data            =[]
        headers         ={
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
        }
        r               = requests.get(url,headers=headers,timeout=10)
        _content        = r.content
        from bs4 import BeautifulSoup
        soup            = BeautifulSoup(_content,"html.parser")
        tr              =soup.select("#eventHistoryTable{0} tr".format(key))

        event_timestamp =[item['event_timestamp'][:10] for item in tr[2:]]
        actual_value    =[float(item.find_all("td")[2].text) if not (item.find_all("td")[2].text =='\xa0') else 0 for item in tr[2:]]

        #data
        for index in range(len(event_timestamp)):
            data.append({
                'date'  :   event_timestamp[index],
                'value' :   actual_value[index],
            })

        event_timestamp =list(reversed(event_timestamp))
        actual_value    =list(reversed(actual_value))

        linegraphobj    = lineGraphController('{0} PMI'.format(country),'date','value')
        base64str       = linegraphobj.getBase64LineChart(event_timestamp, actual_value)

        return {
            'img_str'   :base64str,
            'data'      :data,
        }
    #CPI
    def getCpi(self,url,key,country):
        data            =[]
        headers         ={
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
        }
        r               = requests.get(url,headers=headers,timeout=10)
        _content        = r.content
        from bs4 import BeautifulSoup
        soup            = BeautifulSoup(_content,"html.parser")
        tr              =soup.select("#eventHistoryTable{0} tr".format(key))

        event_timestamp =[item['event_timestamp'][:10] for item in tr[2:]]
        actual_value    =[float(item.find_all("td")[2].text.replace('%', '')) if not (item.find_all("td")[2].text =='\xa0') else 0 for item in tr[2:]]

        #data
        for index in range(len(event_timestamp)):
            data.append({
                'date'  :   event_timestamp[index],
                'value' :   actual_value[index],
            })

        event_timestamp =list(reversed(event_timestamp))
        actual_value    =list(reversed(actual_value))

        linegraphobj    = lineGraphController('{0} CPI'.format(country),'date','value(%)')
        base64str       = linegraphobj.getBase64LineChart(event_timestamp, actual_value)

        return {
            'img_str'   :base64str,
            'data'      :data,
        }

    def getNewHouseOpenInfo(req):
        url='https://www.macromicro.me/charts/data/791'
        session         = requests.Session()
        response        = session.get('https://www.macromicro.me/charts/791/jp-housing-starts')
        print(response.headers['authorization'])
        headers={
            'Accept' : 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate, br',
            'Connection':'keep-alive',
            'Host':'www.macromicro.me',
            'Sec-Fetch-Mode':'cors',
            'Sec-Fetch-Site':'same-origin',
#             'Authorization' : 'Bearer 150820669a56e8cf5d1d704f03de37d8',
            'Referer':'https://www.macromicro.me/charts/791/jp-housing-starts',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest'
        }


        cookie          =session.cookies.get_dict()
#         cookie          ={'PHPSESSID':'u2ip4r61f5mopep3rkehl4bi31'}
#         print(cookie)
        payload         ={}
        r               = requests.get(url,headers=headers,timeout=10,auth=BearerAuth('3pVzwec1Gs1m'))
        response        =r.json()
        print(response)
        newhouseopendata=response['data']['c:791']['s'][0]
        newhousecount   =[]
        date            =[]
        for item in newhouseopendata:
            newhousecount.append(item[1])
            date.append(item[0])

        context         ={
            'newhousecount' :newhousecount,
            'date'          :date,
        }
        return  render(req, 'indicator/newhouseOpeninfo.html', context)

    def getHouseOpen(request):
        appid   ='f507570ff2b0caffb5a69c7fb7ec6b79484d1df9'
        url='http://api.e-stat.go.jp/rest/2.1/app/getStatsData?cdCat02=12%2C13%2C14&cdArea=00001&cdTab=12&cdCat01=11&appId=f507570ff2b0caffb5a69c7fb7ec6b79484d1df9&lang=J&statsDataId=0003114339&metaGetFlg=Y&cntGetFlg=N&sectionHeaderFlg=1'
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            XmlData = response.read()
        result=BeautifulSoup(XmlData,"xml")

#         print(result.STATISTICAL_DATA.find_all('CLASS_OBJ')[3])
#         print(y.STATISTICAL_DATA.find_all('CLASS_OBJ')[3].find_all('CLASS')[0].attrs['code'])
#         print(y.STATISTICAL_DATA.find_all('CLASS_OBJ')[3].find_all('CLASS')[0].attrs['code'])
#         print(result.STATISTICAL_DATA.find_all('VALUE')[0].attrs['time'])
#         print(result.STATISTICAL_DATA.find_all('VALUE')[0].text)
        newhousecount_a   =[]
        newhousecount_b   =[]
        newhousecount_c   =[]
        date            =[]
        for item in result.STATISTICAL_DATA.find_all('VALUE'):
            if item.attrs['cat02']=='12':
                date.append(item.attrs['time'])
                newhousecount_a.append(item.text)
            if item.attrs['cat02']=='13':
                newhousecount_b.append(item.text)
            if item.attrs['cat02']=='14':
                newhousecount_c.append(item.text)
        date                =list(reversed(date))
        newhousecount_a     =list(reversed(newhousecount_a))
        newhousecount_b     =list(reversed(newhousecount_b))
        newhousecount_c     =list(reversed(newhousecount_c))
        context         ={
            'newhousecount_a' :newhousecount_a,
            'newhousecount_b' :newhousecount_b,
            'newhousecount_c' :newhousecount_c,
            'date'            :date,
        }
        return  render(request, 'indicator/newhouseOpeninfo.html', context)











