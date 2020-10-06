from django.shortcuts import render
from django.http.response import HttpResponse
from backend.model.tag import TAG
from backend.model.news import NEWS
from backend.model.tagkubun import TAGKUBUN
from django.db.models import Count
from django.shortcuts import redirect

class tagcontroller:
    def add(request):
        obj = tagcontroller()
        tagname     =request.POST.get('tagname')
        newsid      =request.POST.get('newsid')
        newsobj     = NEWS.objects.get(news_id=newsid)

        if not (newsobj.tag.filter(tag_name = tagname).count() >0):
            if not (TAG.objects.filter(tag_name = tagname).count() >0):
                tagobj  = TAG()
                tagobj.tag_name=tagname
                tagobj.save()
            tagobj =TAG.objects.get(tag_name = tagname)
            newsobj.tag.add(tagobj)

        return HttpResponse('success')

    def removetag(request):
        obj = tagcontroller()
        tagid     =request.POST.get('tagid')
        newsid      =request.POST.get('newsid')
        for news in NEWS.objects.filter(news_id=newsid):
            for tag in news.tag.filter(tag_id=tagid):
                tag.delete()

        return HttpResponse('success')
    #show tag list
    def showtaglist(request):
        taglist           = TAG.objects.annotate(count=Count("news")).order_by('-count')

        context ={
            'taglist'        :taglist,

        }
        return render(request, 'tag/taglist.html', context)

    def showtaginfo(request,tag_id):
        taginfo =TAG.objects.get(tag_id=tag_id)
        kubunlist=TAGKUBUN.objects.all()

        context={
            'taginfo' :taginfo,
            'kubunlist':kubunlist,
            }
        return render(request, 'tag/updatetaginfo.html', context)

    def updatetaginfo(request):
        tagid           =request.POST.get('tag_id')
        kubun_id        =request.POST.get('kubun_id')
        tagname           =request.POST.get('tag_name')

        taginfo         =TAG.objects.get(tag_id=tagid)

        kubun           =TAGKUBUN.objects.get(id=kubun_id)
        taginfo.tag_name=tagname
        taginfo.kubun_id=kubun
        taginfo.save()
        tagname     =request.POST.get('tagname')

        response    =   redirect('/backend/showtagkubunlist/')
        return response