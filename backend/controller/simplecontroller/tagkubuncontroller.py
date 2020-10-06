from django.http.response import HttpResponse
from backend.model.tagkubun import TAGKUBUN
from django.shortcuts import render
from django.shortcuts import redirect

class tagkubuncontroller:
    #show kubun list
    def showtagkubunlist(request):
        tagkubunlist =TAGKUBUN.objects.all()

        context ={
            'tagkubunlist'        :tagkubunlist,

        }
        return render(request, 'tagkubun/tagkubunlist.html', context)

    def add(request):
        tagname     =request.POST.get('tagkubun_name')
        if  tagname =='':
            return HttpResponse('値を入れてください！')
        if not (TAGKUBUN.objects.filter(name = tagname).count() >0):
            kubunobj  = TAGKUBUN()
            kubunobj.name=tagname
            kubunobj.save()
        response    =   redirect('/backend/showtagkubunlist/')
        return response

