from django.shortcuts import render
from django.http.response import HttpResponse
from backend.model.label import LABEL
from backend.model.news import NEWS

class labelcontroller:
    def add(request):
        obj         = labelcontroller()
        label_id    = request.POST.get('label')
        newsid      = request.POST.get('newsid')
        newsobj     = NEWS.objects.get(news_id=newsid)

        if LABEL.objects.filter(label_id=label_id).count() >0 :

            newsobj.label=LABEL.objects.get(label_id=label_id)
            newsobj.save()
            return HttpResponse('success')
        else:
            return HttpResponse('failure')


    def showLabellist(request):
        resultlist           = LABEL.objects.all()

        context ={
            'resultlist'        :resultlist,

        }
        return render(request, 'label/list.html', context)
