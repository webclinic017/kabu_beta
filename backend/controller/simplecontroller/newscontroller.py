from  backend.model.news import NEWS
from  backend.model.tag import TAG
from django.shortcuts import render
from backend.controller.strategy.strategy_context import StrategyContext
from backend.controller.decorate.wordcloud import wordCloud
from backend.controller.decorate.translatecontroller import translateController
from datetime import date
import datetime
from backend.forms.newsform import NewsForm
from django.db.models import Q
import traceback

class newscontroller:
    def shownewsdetail(request,newsid):
        detailinfo              = NEWS.objects.filter(news_id=newsid)
        tags                    = TAG.objects.filter()
        relates_tags            = detailinfo[0].tag.all()
        relates_babel           = detailinfo[0].label
        relates_company         = detailinfo[0].company.all()

        tagstategycontext       = StrategyContext('tag')
        companystategycontext   = StrategyContext('company')

        try:
            translateobj            = translateController(detailinfo[0].detail,'ja','zh')
            translate_content       = translateobj.gettranslatecontent()
        except:
            translate_content       = '翻訳失敗'
            print('翻訳失敗')
        context ={
            'detailinfo'        :detailinfo[0],
            'tags'              : tags,
            'relates_tags'      : relates_tags,
            'relates_babel'     : relates_babel,
            'relates_company'   :relates_company,
            'possible_tag'      :tagstategycontext.getPossibleResult(detailinfo[0].title + detailinfo[0].detail),
            'possible_company'  :companystategycontext.getPossibleResult(detailinfo[0].detail),
            'translate_content' :translate_content,
        }
        return render(request, 'news/news_detail.html', context)

    def getNewsByDate(self,start_date,end_date,company_name):
        detailinfo              = NEWS.objects.filter(
            company__name__icontains=company_name,
            create_date__lte        =end_date,
            create_date__gte        =start_date,
        )

        return  detailinfo

    def getWeekNews(request):
        obj                     = newscontroller()
        today                   = date.today()
        sunday                  = today - datetime.timedelta(today.weekday()+1)
        info                    = obj.getNewsByDate(sunday, today)

        context ={
            'infolist' :info,
            'news_count': len(info),
            }
        return render(request, 'news/news_list.html', context)

    def getMonthNews(request):
        obj                     = newscontroller()
        today                   = date.today()
        month_startday          = today.replace(day=1)
        info                    = obj.getNewsByDate(month_startday, today)
        context ={
            'infolist' :info,
            'news_count': len(info),
            }

        return render(request, 'news/news_list.html', context)

    def searchnews(request):
        form                        = NewsForm(data=request.POST)
        info                        =[]
        news_start_date             =''
        news_end_date               =''
        search_condition            ={}

        if form.is_valid():
            news_start_date             = form.cleaned_data['news_start_date']
            news_end_date               = form.cleaned_data['news_end_date']
            company_name                = form.cleaned_data['company_name']

            if news_start_date is None:
                news_start_date         =datetime.date(2010, 10, 1)
            if news_end_date is None:
                news_end_date           =date.today()
            obj                         = newscontroller()
            info                        = obj.getNewsByDate(news_start_date,news_end_date,company_name)

#             print(''.join(traceback.format_stack()))
            search_condition            ={
                'news_start_date'   :news_start_date.strftime('%Y/%m/%d'),
                'news_end_date'     :news_end_date.strftime('%Y/%m/%d'),
                'company_name'      :company_name,
            }
            context={
                 'infolist'         :info,
                 'news_count'       : len(info),
                 'search_condition' :search_condition
            }
            return render(request, 'news/news_search.html', context)





