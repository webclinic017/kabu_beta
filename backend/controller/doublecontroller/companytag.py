from backend.model.news import NEWS
from django.shortcuts import render
from backend.model.company import COMPANY
from backend.model.tag import TAG
from django.db import connection
from front.models.comany import Company

class companyTag:
    def __init__(self):
        return

    def showcompanyviatag(request,tag_id):
        newslist           = NEWS.objects.filter(tag=tag_id)
        detailinfo         =COMPANY.objects.filter(news__in=newslist)
        companylist        =Company.objects.filter(company_code__in=detailinfo).order_by('-monitor_flag')
        context      ={
            'infolist'        :companylist,
        }
        return render(request, 'companytag/company_list.html', context)

    def gettagviaCompanycode(self,company_code):
        newslist        =[]
        compnaytagobj   = companyTag()
        results         = compnaytagobj.gettagResultViaCompanyCode(company_code)
        for temp in results:
            tag ={}
            tag['tag_id']   =temp[0]
            tag['tag_name'] =temp[1]
            newslist.append(tag)
        return newslist
    #     月別-量価
    def gettagListviaCompanycode(self,company_code):
        newslist        =[]
        compnaytagobj   = companyTag()
        results         = compnaytagobj.gettagResultViaCompanyCode(company_code)
        for temp in results:
            newslist.append(temp[1])
        return newslist


    def gettagResultViaCompanyCode(self,company_code):
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT
                backend_news_tag.tag_id,backend_tag.tag_name
            FROM
                backend_news_tag
            LEFT JOIN backend_news
                ON backend_news.news_id = backend_news_tag.news_id
            LEFT JOIN backend_news_company
                on backend_news_company.news_id=backend_news_tag.news_id
            LEFT JOIN backend_company
                on backend_company.code=backend_news_company.company_id
            LEFT JOIN backend_tag
                ON backend_tag.tag_id = backend_news_tag.tag_id
            WHERE
                backend_company.code={0}
            group by backend_news_tag.tag_id
            """.format(company_code))
        results = cursor.fetchall()
        return results

    def showtagviaCompanycode(request,company_code):

        obj =companyTag()
        context      ={
            'infolist'        :obj.gettagviaCompanycode(company_code),
        }

        return render(request, 'companytag/taglist.html', context)

