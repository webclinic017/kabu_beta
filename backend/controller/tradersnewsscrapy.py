# https://www.traders.co.jp/

from django.http import HttpResponse
import requests,urllib
from    backend.model.news import NEWS
import re
from django.utils import timezone

class Trade:

    def action(self):
        print('hell0')

    def getjapaninfo(self):
        objTrade =Trade()
        urllist = objTrade.getallurl()
        for url in urllist:
            r=requests.get(url, timeout=(3.0, 7.5))
            if not objTrade.insertDB(r):
                break
            print(url)
        return HttpResponse('test')

    #https://www.traders.co.jp/news/news_top.asp?page=1&newscode=1440785&type=1&filter=JP
    #https://www.traders.co.jp/news/news_top.asp?page=2&newscode=1440785&type=1&filter=JP
    #https://www.traders.co.jp/news/news_top.asp?page=3&newscode=1440785&type=1&filter=JP
    def getallurl(self):
        urllist =[]
        for i in range(1,10):
            urllist.append('https://www.traders.co.jp/news/news_top.asp?page={0}&newscode=1440785&type=1&filter=JP'.format(i))
        return urllist

    #insert japan news to DB or info already exsit
    def isInDB(self,url):
        if NEWS.objects.filter(url =url).count() >0:
            return True
        else:
            return False

    def insertDB(self,r):
        from bs4 import BeautifulSoup
        soup                        = BeautifulSoup(r.content, 'html.parser',from_encoding='UTF-8')
        news_list                   = soup.select('div.news_div')
        for i in range(0,len(news_list)):
            try:
                title       =news_list[i].select('span.headline_link')[0].text.replace(' ', '').strip()
                description =news_list[i].select('div.article_sample')[0].text.replace(' ', '').strip()
                class_id    = 2
                onclick     =news_list[i].select('span.headline_link')[0].attrs['onclick']
                pattern     = '.*?(\d+).*'
                result      = re.match(pattern, onclick)
                if result:
                    newsid     = result.group(1)
                    url        = 'https://www.traders.co.jp/news/news_top.asp?newscode={0}&type=1&filter=JP&n=#news_top'.format(newsid)
                    contx      = requests.get("https://www.traders.co.jp/news/news_top.asp?newscode={0}&type=1&filter=JP&n=#news_top".format(newsid), timeout=(3.0, 7.5))
                    contx1     =BeautifulSoup(contx.content, 'html.parser',from_encoding='UTF-8')
                    detail     = contx1.select('#news_article')[0].text

                else:
                    url     =''
                    detail  =''

                if not self.isInDB(url):
                    objnews             =NEWS()
                    objnews.class_id    =class_id
                    objnews.title       =title
                    objnews.description =description
                    objnews.url         =url
                    objnews.detail      =detail
                    objnews.create_date =timezone.datetime.now()


                    objnews.save()
                else:
                    print(title)
                    return  False
            except  Exception as e:
                print(e)

        return  True

    def getchinainfo(self):
        url             = 'https://www.traders.co.jp/news/news_top.asp?page=1&newscode=1440785&type=1&filter={0}'+format('CH')
        print(url)



