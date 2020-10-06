from django.http.response import HttpResponse
from mail.controller.mailcontroller import mailController
from django.shortcuts import render
# Create your views here.

def testSTMP(request):
    obj                         ={}

    obj['Subject']              ='test'
    obj['body']                 ="""\
        """
    obj['to_address']           ='lizhu_zhang@rubygroupe.jp'

    mailControllerobj           = mailController(obj['to_address'])
    if mailControllerobj.getTemplateMail(obj) == 'success':
        return HttpResponse('success')
    else:
        return HttpResponse('fail')