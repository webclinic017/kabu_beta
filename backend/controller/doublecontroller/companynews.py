from backend.model.news import NEWS
from django.shortcuts import render
from backend.model.company import COMPANY
from front.models.comany import Company
from backend.controller.simplecontroller import companycontroller
from django.http.response import HttpResponse

class companynews:

    def add(request):
        company_code        =request.POST.get('company_code')
        newsid              =request.POST.get('newsid')
        if not (company_code ==''):
            newsobj             = NEWS.objects.get(news_id=newsid)
            if not (newsobj.company.filter(code = company_code).count() >0):
                if not (COMPANY.objects.filter(code = company_code).count() >0):
                    companyobj          = COMPANY()
                    companyobj.code=int(company_code)
                    try:
                        companyobj.name     = Company.objects.get(company_code=(company_code)).company_name
                    except:
                        print("銘柄名が取得できません")
                    companyobj.save()
                companyobj =COMPANY.objects.get(code = company_code)
                newsobj.company.add(companyobj)
        return HttpResponse('success')

    #removecompany
    def removecompany(request):
        newsid          =request.POST.get('newsid')
        companycode       =request.POST.get('companycode')
        for news in NEWS.objects.filter(news_id=newsid):
            for company in news.company.filter(code=companycode):
                company.delete()

        return HttpResponse('success')

    def showcompanynewsViacompanycode(request,company_code):
        companylist          =COMPANY.objects.filter(code=company_code)
        detailinfo           = NEWS.objects.filter(company__in=companylist)
        context ={
            'infolist'        :detailinfo,
            'companycode'     :company_code,
        }
        return render(request, 'companynews/list.html', context)

    def getnewstxtViacompanycode(self,company_code):
        result              =""
        companylist          =COMPANY.objects.filter(code=company_code)
        detailinfo           = NEWS.objects.filter(company__in=companylist)
        for news in detailinfo:
            result+=news.detail
        return result


