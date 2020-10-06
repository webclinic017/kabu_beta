from  backend.model.news import NEWS
from  backend.model.tag import TAG
from django.shortcuts import render
from django.http.response import HttpResponse


class showjpinfo:
    def list(request):
        infolist = NEWS.objects.filter(del_flg=0,checked_flg=0).order_by('-news_id')

        context ={
            'infolist' :infolist,
            'news_count': len(infolist),
            }
        return render(request, 'news/news_list.html', context)

    def check(request,newsid):
        newsid    =int(newsid)
        newsobj  = NEWS.objects.get(del_flg=0,news_id=newsid)
        newsobj.checked_flg=1
        newsobj.save()

        return HttpResponse('success')


    #add memo
    def addmemo(request,memo):
        return HttpResponse('success')