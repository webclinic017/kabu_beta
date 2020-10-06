from backend.model.memo import MEMO

class memocontroller:
    def add(request):
        obj             = memocontroller()
        start_date      = request.POST.get('start_date')
        end_date        = request.POST.get('end_date')
        event_name      = request.POST.get('event_name')

        memoobj         = MEMO.objects.get(event_name=event_name)

        if MEMO.objects.filter(label_id=label_id).count() >0 :
            return HttpResponse('success')
        else:
            return HttpResponse('failure')