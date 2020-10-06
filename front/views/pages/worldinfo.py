from django.http.response import HttpResponse
import requests,urllib
import tradingeconomics as te
from django.shortcuts import render
from urllib import request


def getworldinfo(request):
    context={}
    return render(request, 'worldinfo.html', context)