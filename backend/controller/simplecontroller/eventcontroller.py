from backend.model.event import EVENT
from django.http.response import HttpResponse
from datetime import datetime
from django.shortcuts import render

class eventcontroller:
    def add(request):
        obj             = eventcontroller()
        start_date      = request.POST.get('event_startdate')
        end_date        = request.POST.get('event_enddate')
        event_name      = request.POST.get('event_name')

        start_date      =datetime.strptime(start_date, "%Y/%m/%d").date()
        end_date        =datetime.strptime(end_date, "%Y/%m/%d").date()
        if EVENT.objects.filter(name=event_name).count() == 0 :
            eventobj                = EVENT()
            eventobj.name           = event_name
            eventobj.start_date     = start_date
            eventobj.end_date       = end_date
            eventobj.save()
            return HttpResponse('success')
        else:
            return HttpResponse('failure')


    def showeventlist(request):
        resultlist =EVENT.objects.all()

        context ={
            'resultlist'        :resultlist,

        }

        return render(request, 'event/eventlist.html', context)